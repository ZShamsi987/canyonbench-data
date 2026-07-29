#!/usr/bin/env python3
"""Point the annotation task files and assignment sheets at the corrected frames.

This rewrites only the image URL/path prefix, from `frames/` to
`frames_corrected/`. Every assignment, split, ordering and task id is left
byte-identical, so annotators keep the same workload and the same task sequence
they already have. Run after `build_corrected_frames.py`.

Use --revert to point everything back at the raw frames.
"""

from __future__ import annotations

import argparse
from pathlib import Path

RAW = "frames/"
CORRECTED = "frames_corrected/"

TARGETS = [
    "label-studio/tasks/*.json",
    "annotation/assignments/*.csv",
    "annotation/registration_candidates.csv",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--revert", action="store_true")
    args = parser.parse_args()

    src, dst = (CORRECTED, RAW) if args.revert else (RAW, CORRECTED)

    changed = 0
    for pattern in TARGETS:
        for path in sorted(args.root.glob(pattern)):
            text = path.read_text()
            if src not in text:
                continue
            path.write_text(text.replace(src, dst), newline="\n")
            n = text.count(src)
            changed += n
            print(f"{path}: {n} references -> {dst}")

    print(f"\nrewrote {changed} image references to {dst}")
    if not args.revert:
        print("frames/ is untouched and remains the authoritative released imagery.")


if __name__ == "__main__":
    main()
