#!/usr/bin/env python3
"""Build colour-corrected annotation frames from the released raw frames.

Why this exists
---------------
The WORLD-10 camera recorded with an uncorrected white balance. At altitude the
whole scene is shifted strongly toward blue/violet, which makes green vegetation
read as grey-olive and makes shadowed rock read as blue. Annotators cannot apply
manual rule A-1 ("hue reads green") to imagery in that state, and the first
calibration checkpoint showed four annotators producing four different answers
because of it.

This script removes the *colour cast* only. It does not remove haze. Veiling
contrast loss is a separate physical effect that is preserved deliberately, so
the `clarity` quality flag still measures something real.

Method
------
For each frame:

1. Build a terrain reference population, excluding
   - dark pixels (water, deep shadow),
   - near-clipped bright pixels,
   - pixels that are already green-dominant, so that vegetation does not drag
     the reference toward green and suppress itself.
2. Take the per-channel median of that population.
3. Scale each channel so the median lands on a fixed bare-desert reference
   colour measured from USGS NAIP 2023 over the flight corridor.

The target is a single global constant, so every frame's terrain is normalised
to the same appearance. This deliberately discards real between-frame geology
and illumination differences: the output is an *annotation aid*, not a
radiometric product. `frames/` remains the authoritative released imagery.

Outputs
-------
frames_corrected/<phase>/<image>          corrected JPEGs
metadata/colour_correction.csv            per-frame gains and diagnostics
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import numpy as np
from PIL import Image

# Bare-desert median measured from USGS NAIP 2023 (public domain) over the
# Glen Canyon / Page corridor the flight crosses. See metadata/provenance.yaml.
TARGET_RGB = np.array([183.0, 136.0, 102.0])

DARK_V = 0.24  # below this is water or deep shadow, not terrain
BRIGHT_V = 0.92  # above this is near-clipped, unreliable for a reference
MIN_REFERENCE_PX = 20000
GAIN_LIMITS = (0.40, 3.00)

FIELDS = [
    "image",
    "phase",
    "ref_r",
    "ref_g",
    "ref_b",
    "gain_r",
    "gain_g",
    "gain_b",
    "reference_px",
    "clipped_after",
    "green_fraction",
    "green_largest_blob_px",
    "sha256",
]

# Green as manual rule A-1 defines it, applied to the corrected image.
#
# The upper hue bound is 150 deg, not 170. Swimming pools, lined industrial
# ponds and shallow turquoise water sit at 165-200 deg and were inflating this
# measurement by roughly 2x on frames that contain the town of Page. The value
# ceiling excludes those same bright cyan surfaces; living vegetation in this
# scene is dark (typical corrected RGB around 60,85,55).
GREEN_HUE = (70.0, 150.0)
GREEN_MIN_SAT = 0.15
GREEN_MIN_VALUE = 0.18
GREEN_MAX_VALUE = 0.70


def green_stats(rgb: np.ndarray) -> tuple[float, int]:
    """Fraction of the corrected frame that reads green, and the largest patch.

    Measured on the float image *before* JPEG encoding. Re-encoding introduces
    chroma artefacts that inflate this figure by up to ~50%, so any published
    number must come from here rather than from the delivered JPEG.
    """
    arr = np.clip(rgb, 0, 255) / 255.0
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    diff = mx - mn
    sat = np.where(mx > 0, diff / np.maximum(mx, 1e-9), 0.0)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    hue = np.zeros_like(mx)
    safe = diff > 1e-9
    idx = safe & (mx == g)
    hue[idx] = 60.0 * (2.0 + (b[idx] - r[idx]) / diff[idx])
    idx = safe & (mx == b)
    hue[idx] = 60.0 * (4.0 + (r[idx] - g[idx]) / diff[idx])
    idx = safe & (mx == r)
    hue[idx] = 60.0 * (((g[idx] - b[idx]) / diff[idx]) % 6.0)

    mask = (
        (hue >= GREEN_HUE[0])
        & (hue <= GREEN_HUE[1])
        & (sat >= GREEN_MIN_SAT)
        & (mx >= GREEN_MIN_VALUE)
        & (mx <= GREEN_MAX_VALUE)
    )
    if not mask.any():
        return 0.0, 0
    try:
        from scipy import ndimage

        labels, count = ndimage.label(mask)
        largest = (
            int(np.bincount(labels.ravel())[1:].max()) if count else 0
        )
    except Exception:
        largest = -1
    return float(mask.mean()), largest


def terrain_reference(rgb: np.ndarray) -> tuple[np.ndarray, int]:
    """Median RGB of the frame's bare-terrain population."""
    value = rgb.max(axis=2) / 255.0
    usable = (value > DARK_V) & (value < BRIGHT_V)
    # Drop green-dominant pixels so vegetation does not bias its own correction.
    not_green = rgb[..., 1] <= rgb[..., 0]
    population = usable & not_green
    if population.sum() < MIN_REFERENCE_PX:
        population = usable
    if population.sum() < MIN_REFERENCE_PX:
        population = np.ones(value.shape, dtype=bool)
    ref = np.array([np.median(rgb[..., i][population]) for i in range(3)])
    return ref, int(population.sum())


def correct(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    ref, n = terrain_reference(rgb)
    gain = np.clip(TARGET_RGB / np.maximum(ref, 1.0), *GAIN_LIMITS)
    out = np.clip(rgb * gain, 0, 255)
    return out, ref, gain, n


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=Path, default=Path("frames"))
    parser.add_argument("--out", type=Path, default=Path("frames_corrected"))
    parser.add_argument(
        "--manifest", type=Path, default=Path("metadata/colour_correction.csv")
    )
    parser.add_argument("--quality", type=int, default=90)
    args = parser.parse_args()

    rows: list[dict[str, object]] = []
    for phase_dir in sorted(p for p in args.frames.iterdir() if p.is_dir()):
        target_dir = args.out / phase_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted(phase_dir.glob("*.jpg")):
            rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
            out, ref, gain, n = correct(rgb)
            dst = target_dir / src.name
            frac, blob = green_stats(out)
            Image.fromarray(out.astype(np.uint8)).save(dst, quality=args.quality)
            rows.append(
                {
                    "image": src.name,
                    "phase": phase_dir.name,
                    "ref_r": round(ref[0], 2),
                    "ref_g": round(ref[1], 2),
                    "ref_b": round(ref[2], 2),
                    "gain_r": round(gain[0], 4),
                    "gain_g": round(gain[1], 4),
                    "gain_b": round(gain[2], 4),
                    "reference_px": n,
                    "clipped_after": round(float((out >= 255).mean()), 6),
                    "green_fraction": round(frac, 6),
                    "green_largest_blob_px": blob,
                    "sha256": sha256(dst),
                }
            )

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"corrected {len(rows)} frames -> {args.out}")
    print(f"manifest -> {args.manifest}")


if __name__ == "__main__":
    main()
