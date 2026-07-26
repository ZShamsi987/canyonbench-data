#!/usr/bin/env python3
"""Prepare a private, reproducible annotation and registration handoff."""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
    "image",
    "image_path",
    "elapsed_s",
    "phase",
    "segment_id",
    "spatial_block",
    "split",
}
PUBLIC_SPLIT_FIELDS = ("image", "segment_id", "spatial_block", "split")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("Sampled frame manifest is empty")
    missing = REQUIRED_COLUMNS - set(rows[0])
    if missing:
        raise ValueError(
            f"Sampled frame manifest is missing columns: {sorted(missing)}"
        )
    return sorted(rows, key=lambda row: int(row["elapsed_s"]))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def validate_splits(rows: list[dict[str, str]]) -> None:
    split_names = {row["split"] for row in rows}
    if split_names != {"train", "validation", "test"}:
        raise ValueError(
            f"Expected train/validation/test splits, found {sorted(split_names)}"
        )
    for key in ("segment_id", "spatial_block"):
        assignments: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            assignments[row[key]].add(row["split"])
        leaking = sorted(
            value for value, splits in assignments.items() if len(splits) > 1
        )
        if leaking:
            raise ValueError(f"{key} values leak across splits: {leaking[:5]}")


def allocate_quotas(
    groups: dict[tuple[str, str], list[dict[str, str]]], total: int
) -> dict[tuple[str, str], int]:
    if total < len(groups):
        raise ValueError(
            "Selection size is too small to cover every phase/split stratum"
        )
    population = sum(len(group) for group in groups.values())
    quotas = {key: 1 for key in groups}
    remaining = total - len(groups)
    exact = {key: remaining * len(group) / population for key, group in groups.items()}
    for key in groups:
        quotas[key] += int(exact[key])
    leftover = total - sum(quotas.values())
    ranked = sorted(groups, key=lambda key: (exact[key] % 1, key), reverse=True)
    for key in ranked[:leftover]:
        quotas[key] += 1
    return quotas


def select_stratified(
    rows: list[dict[str, str]],
    total: int,
    *,
    excluded_images: set[str] | None = None,
) -> list[dict[str, str]]:
    excluded = excluded_images or set()
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["image"] not in excluded:
            groups[(row["phase"], row["split"])].append(row)
    quotas = allocate_quotas(groups, total)
    selected: list[dict[str, str]] = []
    for key in sorted(groups):
        group = groups[key]
        quota = min(quotas[key], len(group))
        indices = [
            min(int((index + 0.5) * len(group) / quota), len(group) - 1)
            for index in range(quota)
        ]
        selected.extend(group[index] for index in indices)
    if len(selected) != total or len({row["image"] for row in selected}) != total:
        raise ValueError("Could not construct a unique stratified selection")
    return sorted(selected, key=lambda row: int(row["elapsed_s"]))


def materialize(source: Path, target: Path, mode: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if source.samefile(target):
            return
        raise FileExistsError(f"Refusing to overwrite existing frame: {target}")
    if mode == "hardlink":
        os.link(source, target)
    else:
        shutil.copy2(source, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sampled_csv", type=Path)
    parser.add_argument("frames_root", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("splits_output", type=Path)
    parser.add_argument("--mode", choices=("hardlink", "copy"), default="hardlink")
    args = parser.parse_args()

    rows = read_rows(args.sampled_csv)
    validate_splits(rows)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    package_rows: list[dict[str, str]] = []
    tasks: list[dict[str, Any]] = []
    for row in rows:
        phase_dir = row["phase"].lower()
        source = (args.frames_root / row["image"]).resolve()
        target = output / "frames" / phase_dir / row["image"]
        if not source.is_file():
            raise FileNotFoundError(source)
        materialize(source, target, args.mode)
        relative = target.relative_to(output).as_posix()
        package_row = dict(row)
        package_row["image_path"] = relative
        package_rows.append(package_row)
        tasks.append(
            {
                "data": {"image": f"/data/local-files/?d={relative}"},
                "meta": {
                    "image": row["image"],
                    "elapsed_s": int(row["elapsed_s"]),
                    "phase": row["phase"],
                    "segment_id": row["segment_id"],
                    "split": row["split"],
                },
            }
        )

    manifest_fields = tuple(package_rows[0])
    write_csv(
        output / "manifests" / "frames_sampled.csv", package_rows, manifest_fields
    )
    write_csv(args.splits_output, rows, PUBLIC_SPLIT_FIELDS)
    (output / "label_studio_tasks.json").write_text(
        json.dumps(tasks, indent=2) + "\n", encoding="utf-8"
    )

    calibration = select_stratified(rows, 30)
    calibration_images = {row["image"] for row in calibration}
    qualification = select_stratified(rows, 12, excluded_images=calibration_images)
    selection_fields = (
        "image",
        "elapsed_s",
        "phase",
        "segment_id",
        "spatial_block",
        "split",
    )
    write_csv(
        output / "assignments" / "shared_calibration_30.csv",
        calibration,
        selection_fields,
    )
    qualification_rows = [
        {**row, "gold_status": "pending_lead_adjudication"} for row in qualification
    ]
    write_csv(
        output / "assignments" / "qualification_candidates_12.csv",
        qualification_rows,
        (*selection_fields, "gold_status"),
    )

    by_segment: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_segment[row["segment_id"]].append(row)
    assignments: list[dict[str, Any]] = []
    for segment, members in sorted(by_segment.items()):
        assignments.append(
            {
                "segment_id": segment,
                "phase": members[0]["phase"],
                "split": members[0]["split"],
                "elapsed_start_s": min(int(row["elapsed_s"]) for row in members),
                "elapsed_end_s": max(int(row["elapsed_s"]) for row in members),
                "frame_count": len(members),
                "annotator_1": "",
                "annotator_2": "",
            }
        )
    assignment_fields = (
        "segment_id",
        "phase",
        "split",
        "elapsed_start_s",
        "elapsed_end_s",
        "frame_count",
        "annotator_1",
        "annotator_2",
    )
    write_csv(
        output / "assignments" / "segment_assignments.csv",
        assignments,
        assignment_fields,
    )

    registration_rows = [
        {
            "image": row["image"],
            "phase": row["phase"],
            "elapsed_s": row["elapsed_s"],
            "segment_id": row["segment_id"],
            "split": row["split"],
            "registration_status": "pending",
        }
        for row in rows
    ]
    write_csv(
        output / "registration_candidates.csv",
        registration_rows,
        (
            "image",
            "phase",
            "elapsed_s",
            "segment_id",
            "split",
            "registration_status",
        ),
    )

    counts = Counter(row["split"] for row in rows)
    readme = f"""# CanyonBench private curation package

This directory is intentionally ignored by Git. It contains {len(rows)} sampled frames
({counts["train"]} train, {counts["validation"]} validation, {counts["test"]} test).

Set `LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT` to this directory, enable local-file
serving in Label Studio, and import `label_studio_tasks.json` into each task project.
Use the XML interfaces in the repository's `label-studio/` directory and follow
`ANNOTATION.md` plus `docs/annotation-manual.md`.

The 30-frame calibration set is labeled by every annotator. The 12 qualification
candidates require lead-created gold labels before they can gate annotators.
Assign two annotators to every row in `assignments/segment_assignments.csv`.
Registration candidates follow `docs/registration.md`; no registration result is
implied by inclusion in that manifest.
"""
    (output / "README.md").write_text(readme, encoding="utf-8")
    print(
        f"Prepared {len(rows)} frames, {len(assignments)} segments, "
        f"{len(calibration)} calibration frames, and {len(qualification)} "
        f"qualification candidates in {output}"
    )


if __name__ == "__main__":
    main()
