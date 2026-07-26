#!/usr/bin/env python3
"""Build the public, four-coauthor CanyonBench annotation handoff."""

from __future__ import annotations

import argparse
import csv
import filecmp
import hashlib
import itertools
import json
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote

DEFAULT_ANNOTATORS = ("A1", "A2", "A3", "A4")
DEFAULT_ANNOTATOR_NAMES = {
    "A1": "Atharva",
    "A2": "Pranav G.",
    "A3": "Kunsh",
    "A4": "Prabhav",
}
DEFAULT_BASE_URL = (
    "https://raw.githubusercontent.com/ZShamsi987/canyonbench-data/main/frames"
)
REQUIRED_COLUMNS = {
    "image",
    "image_path",
    "elapsed_s",
    "phase",
    "segment_id",
    "spatial_block",
    "split",
}
SELECTION_FIELDS = (
    "image",
    "image_url",
    "elapsed_s",
    "phase",
    "segment_id",
    "spatial_block",
    "split",
)


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
    rows.sort(key=lambda row: int(row["elapsed_s"]))
    if len({row["image"] for row in rows}) != len(rows):
        raise ValueError("Sampled frame manifest contains duplicate image keys")
    return rows


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fields: tuple[str, ...],
) -> None:
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


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def validate_splits(rows: list[dict[str, str]]) -> None:
    if {row["split"] for row in rows} != {"train", "validation", "test"}:
        raise ValueError("Expected train, validation, and test rows")
    for field in ("segment_id", "spatial_block"):
        assignments: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            assignments[row[field]].add(row["split"])
        leaking = sorted(
            value for value, splits in assignments.items() if len(splits) > 1
        )
        if leaking:
            raise ValueError(f"{field} values leak across splits: {leaking[:5]}")


def allocate_quotas(
    groups: dict[tuple[str, str], list[dict[str, str]]],
    total: int,
) -> dict[tuple[str, str], int]:
    if total < len(groups):
        raise ValueError("Selection is too small to cover every phase/split stratum")
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
        if source.samefile(target) or filecmp.cmp(source, target, shallow=False):
            return
        raise FileExistsError(f"Refusing to overwrite a different frame: {target}")
    if mode == "hardlink":
        os.link(source, target)
    else:
        shutil.copy2(source, target)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def public_row(row: dict[str, str], base_url: str) -> dict[str, str]:
    phase_dir = row["phase"].lower()
    return {
        **row,
        "image_path": f"frames/{phase_dir}/{row['image']}",
        "image_url": f"{base_url.rstrip('/')}/{phase_dir}/{quote(row['image'])}",
    }


def assignment_pairs(
    rows: list[dict[str, str]],
    annotators: tuple[str, ...],
    shared_images: set[str],
) -> tuple[dict[str, tuple[str, str]], list[dict[str, Any]]]:
    if len(annotators) != 4 or len(set(annotators)) != 4:
        raise ValueError("Exactly four unique annotator ids are required")
    pairs = list(itertools.combinations(annotators, 2))
    pair_load = {pair: 0 for pair in pairs}
    annotator_load = {annotator: 0 for annotator in annotators}
    phase_load = {annotator: Counter() for annotator in annotators}
    split_load = {annotator: Counter() for annotator in annotators}

    by_segment: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_segment[row["segment_id"]].append(row)

    segment_inputs: list[
        tuple[str, int, list[dict[str, str]], Counter[str], Counter[str]]
    ] = []
    for segment_id, members in by_segment.items():
        production = [row for row in members if row["image"] not in shared_images]
        segment_inputs.append(
            (
                segment_id,
                len(production),
                members,
                Counter(row["phase"] for row in production),
                Counter(row["split"] for row in production),
            )
        )

    assigned: dict[str, tuple[str, str]] = {}
    for segment_id, weight, members, phases, splits in sorted(
        segment_inputs,
        key=lambda item: (-item[1], item[0]),
    ):

        def score(pair: tuple[str, str]) -> tuple[Any, ...]:
            next_pair_loads = [
                pair_load[candidate] + (weight if candidate == pair else 0)
                for candidate in pairs
            ]
            next_annotator_loads = {
                annotator: annotator_load[annotator]
                + (weight if annotator in pair else 0)
                for annotator in annotators
            }
            values = list(next_annotator_loads.values())
            stratum_penalty = sum(
                (
                    phase_load[annotator][phase]
                    + (phases[phase] if annotator in pair else 0)
                )
                ** 2
                for annotator in annotators
                for phase in ("Launching", "Floating")
            ) + sum(
                (
                    split_load[annotator][split]
                    + (splits[split] if annotator in pair else 0)
                )
                ** 2
                for annotator in annotators
                for split in ("train", "validation", "test")
            )
            return (
                max(next_pair_loads) - min(next_pair_loads),
                max(values) - min(values),
                max(next_pair_loads),
                stratum_penalty,
                pair,
            )

        pair = min(pairs, key=score)
        assigned[segment_id] = pair
        pair_load[pair] += weight
        for annotator in pair:
            annotator_load[annotator] += weight
            phase_load[annotator].update(phases)
            split_load[annotator].update(splits)

    segment_rows: list[dict[str, Any]] = []
    for segment_id, members in sorted(by_segment.items()):
        calibration_count = sum(
            row.get("assignment_type") == "calibration" for row in members
        )
        qualification_count = sum(
            row.get("assignment_type") == "qualification" for row in members
        )
        production_count = len(members) - calibration_count - qualification_count
        pair = assigned[segment_id]
        segment_rows.append(
            {
                "segment_id": segment_id,
                "phase": members[0]["phase"],
                "split": members[0]["split"],
                "elapsed_start_s": min(int(row["elapsed_s"]) for row in members),
                "elapsed_end_s": max(int(row["elapsed_s"]) for row in members),
                "frame_count_total": len(members),
                "production_frame_count": production_count,
                "calibration_frame_count": calibration_count,
                "qualification_frame_count": qualification_count,
                "annotator_1": pair[0],
                "annotator_2": pair[1],
            }
        )
    return assigned, segment_rows


def task(row: dict[str, str], assignment_type: str) -> dict[str, Any]:
    return {
        "data": {"image": row["image_url"]},
        "meta": {
            "image": row["image"],
            "elapsed_s": int(row["elapsed_s"]),
            "phase": row["phase"],
            "segment_id": row["segment_id"],
            "split": row["split"],
            "assignment_type": assignment_type,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Publish sampled frames and deterministic A1-A4 Label Studio worklists"
        )
    )
    parser.add_argument("sampled_csv", type=Path)
    parser.add_argument("frames_root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("."))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--annotators",
        nargs=4,
        default=DEFAULT_ANNOTATORS,
        metavar=("ID1", "ID2", "ID3", "ID4"),
    )
    parser.add_argument("--mode", choices=("hardlink", "copy"), default="hardlink")
    args = parser.parse_args()

    rows = read_rows(args.sampled_csv)
    validate_splits(rows)
    output = args.output.resolve()
    annotators = tuple(args.annotators)

    public_rows = [public_row(row, args.base_url) for row in rows]
    calibration = select_stratified(public_rows, 30)
    calibration_images = {row["image"] for row in calibration}
    qualification = select_stratified(
        public_rows,
        12,
        excluded_images=calibration_images,
    )
    qualification_images = {row["image"] for row in qualification}
    if calibration_images & qualification_images:
        raise AssertionError("Calibration and qualification selections overlap")

    typed_rows: list[dict[str, str]] = []
    for row in public_rows:
        if row["image"] in calibration_images:
            assignment_type = "calibration"
        elif row["image"] in qualification_images:
            assignment_type = "qualification"
        else:
            assignment_type = "production"
        typed_rows.append({**row, "assignment_type": assignment_type})

    shared_images = calibration_images | qualification_images
    assigned, segment_rows = assignment_pairs(
        typed_rows,
        annotators,
        shared_images,
    )

    checksum_lines: list[str] = []
    for row in typed_rows:
        source = (args.frames_root / row["image"]).resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        target = output / row["image_path"]
        materialize(source, target, args.mode)
        checksum_lines.append(f"{sha256(target)}  {row['image_path']}")
    (output / "metadata").mkdir(parents=True, exist_ok=True)
    (output / "metadata" / "frame_checksums.sha256").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
    )

    manifest_fields = tuple(typed_rows[0])
    write_csv(output / "metadata" / "frames_sampled.csv", typed_rows, manifest_fields)

    assignment_root = output / "annotation" / "assignments"
    selection_fields = (*SELECTION_FIELDS, "assignment_type")
    calibration_typed = [
        {**row, "assignment_type": "calibration"} for row in calibration
    ]
    qualification_typed = [
        {
            **row,
            "assignment_type": "qualification",
            "gold_status": "pending_lead_adjudication",
        }
        for row in qualification
    ]
    write_csv(
        assignment_root / "shared_calibration_30.csv",
        calibration_typed,
        selection_fields,
    )
    write_csv(
        assignment_root / "qualification_candidates_12.csv",
        qualification_typed,
        (*selection_fields, "gold_status"),
    )
    write_csv(
        assignment_root / "segment_assignments.csv",
        segment_rows,
        (
            "segment_id",
            "phase",
            "split",
            "elapsed_start_s",
            "elapsed_end_s",
            "frame_count_total",
            "production_frame_count",
            "calibration_frame_count",
            "qualification_frame_count",
            "annotator_1",
            "annotator_2",
        ),
    )

    roster_rows = [
        {
            "annotator_id": annotator,
            "coauthor_name": DEFAULT_ANNOTATOR_NAMES.get(annotator, ""),
            "label_studio_email": "",
            "qualification_status": (
                "waived_by_lead" if annotator in DEFAULT_ANNOTATOR_NAMES else "pending"
            ),
            "qualification_date": (
                "2026-07-26" if annotator in DEFAULT_ANNOTATOR_NAMES else ""
            ),
            "notes": (
                "Previously tested and approved by Zafir; starts at calibration"
                if annotator in DEFAULT_ANNOTATOR_NAMES
                else ""
            ),
        }
        for annotator in annotators
    ]
    write_csv(
        output / "annotation" / "annotator_roster.csv",
        roster_rows,
        (
            "annotator_id",
            "coauthor_name",
            "label_studio_email",
            "qualification_status",
            "qualification_date",
            "notes",
        ),
    )

    task_root = output / "label-studio" / "tasks"
    write_json(
        task_root / "all_frames_377.json",
        [task(row, row["assignment_type"]) for row in typed_rows],
    )
    write_json(
        task_root / "shared_calibration_30.json",
        [task(row, "calibration") for row in calibration],
    )
    write_json(
        task_root / "qualification_12.json",
        [task(row, "qualification") for row in qualification],
    )

    workload_rows: list[dict[str, Any]] = []
    project_rows: list[dict[str, str]] = []
    stage_info = (
        (
            "QUALIFICATION",
            "qualification_12.json",
            12,
            "waived for current team; do not create",
        ),
        (
            "CALIBRATION",
            "shared_calibration_30.json",
            30,
            "qualification waived by Zafir; start here",
        ),
        (
            "PRODUCTION",
            "{annotator}_production.json",
            None,
            "calibration checkpoint and final reviewed",
        ),
    )
    task_info = (
        ("MASK", "vegetation-mask.xml"),
        ("PRESENCE", "presence.xml"),
        ("QUALITY", "quality.xml"),
    )

    for annotator in annotators:
        production = [
            row
            for row in typed_rows
            if row["assignment_type"] == "production"
            and annotator in assigned[row["segment_id"]]
        ]
        write_csv(
            assignment_root / f"{annotator}_production.csv",
            production,
            selection_fields,
        )
        write_json(
            task_root / f"{annotator}_production.json",
            [task(row, "production") for row in production],
        )
        unique_images = len(production) + len(calibration) + len(qualification)
        workload_rows.append(
            {
                "annotator_id": annotator,
                "production_frames": len(production),
                "calibration_frames": len(calibration),
                "qualification_frames": len(qualification),
                "total_unique_frames": unique_images,
                "mask_submissions": unique_images,
                "presence_submissions": unique_images,
                "quality_submissions": unique_images,
                "total_submissions": unique_images * 3,
            }
        )
        for stage, filename, fixed_count, starts_after in stage_info:
            task_filename = filename.format(annotator=annotator)
            count = fixed_count if fixed_count is not None else len(production)
            for task_name, config_filename in task_info:
                project_rows.append(
                    {
                        "annotator_id": annotator,
                        "stage": stage,
                        "task": task_name,
                        "project_name": (f"CB-{annotator}-{stage[:4]}-{task_name}"),
                        "label_config": (f"label-studio/{config_filename}"),
                        "task_file": f"label-studio/tasks/{task_filename}",
                        "image_count": str(count),
                        "start_after": starts_after,
                    }
                )

    write_csv(
        assignment_root / "workload_summary.csv",
        workload_rows,
        (
            "annotator_id",
            "production_frames",
            "calibration_frames",
            "qualification_frames",
            "total_unique_frames",
            "mask_submissions",
            "presence_submissions",
            "quality_submissions",
            "total_submissions",
        ),
    )
    write_csv(
        output / "label-studio" / "project_plan.csv",
        project_rows,
        (
            "annotator_id",
            "stage",
            "task",
            "project_name",
            "label_config",
            "task_file",
            "image_count",
            "start_after",
        ),
    )

    registration_rows = [
        {
            "image": row["image"],
            "image_url": row["image_url"],
            "phase": row["phase"],
            "elapsed_s": row["elapsed_s"],
            "segment_id": row["segment_id"],
            "split": row["split"],
            "registration_status": "blocked_pending_reference_license",
            "registrar": "",
            "checker": "",
        }
        for row in typed_rows
    ]
    write_csv(
        output / "annotation" / "registration_candidates.csv",
        registration_rows,
        (
            "image",
            "image_url",
            "phase",
            "elapsed_s",
            "segment_id",
            "split",
            "registration_status",
            "registrar",
            "checker",
        ),
    )

    production_counts = Counter(
        row["image"]
        for annotator in annotators
        for row in typed_rows
        if row["assignment_type"] == "production"
        and annotator in assigned[row["segment_id"]]
    )
    if set(production_counts.values()) != {2}:
        raise AssertionError("Every production image must have exactly two assignees")
    loads = [row["production_frames"] for row in workload_rows]
    if max(loads) - min(loads) > 1:
        raise AssertionError(f"Production workload is not balanced: {loads}")

    print(
        "Prepared public annotation release: "
        f"{len(rows)} frames; "
        f"{len(calibration)} calibration; "
        f"{len(qualification)} qualification; "
        f"production loads {dict(zip(annotators, loads, strict=True))}"
    )


if __name__ == "__main__":
    main()
