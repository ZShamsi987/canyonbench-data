#!/usr/bin/env python3
"""Validate checked-in example JSONL records with only the standard library."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from create_label_studio_projects import LabelStudio, plan_rows

ROOT = Path(__file__).resolve().parents[1]
IMAGE = re.compile(r"^img_\d{6,}\.jpg$")
FEATURES = ("water", "road", "building", "forest", "snow", "field")
ANNOTATORS = ("A1", "A2", "A3", "A4")


class MockResponse:
    def __init__(self, payload: object) -> None:
        self.content = json.dumps(payload).encode()

    def __enter__(self) -> MockResponse:
        return self

    def __exit__(self, *_args: object) -> bool:
        return False

    def read(self) -> bytes:
        return self.content


def validate_label_studio_authentication() -> None:
    """Keep both supported Label Studio token paths working."""

    def legacy_urlopen(
        request: urllib.request.Request,
        timeout: int,
    ) -> MockResponse:
        assert timeout == 60
        assert request.get_header("Authorization") == "Token legacy-secret"
        return MockResponse({"results": [{"title": "legacy-ok"}]})

    with patch("urllib.request.urlopen", legacy_urlopen):
        assert LabelStudio(
            "http://label-studio",
            "legacy-secret",
        ).project_titles() == {"legacy-ok"}

    personal_calls: list[tuple[str, str | None]] = []

    def personal_urlopen(
        request: urllib.request.Request,
        timeout: int,
    ) -> MockResponse:
        assert timeout == 60
        authorization = request.get_header("Authorization")
        personal_calls.append((request.full_url, authorization))
        if request.full_url.endswith("/api/token/refresh"):
            assert authorization is None
            assert json.loads(request.data) == {"refresh": "personal-secret"}
            return MockResponse({"access": "short-lived-access"})
        if authorization == "Token personal-secret":
            raise urllib.error.HTTPError(
                request.full_url,
                401,
                "Unauthorized",
                {},
                io.BytesIO(b"invalid legacy token"),
            )
        assert authorization == "Bearer short-lived-access"
        return MockResponse({"results": [{"title": "personal-ok"}]})

    with patch("urllib.request.urlopen", personal_urlopen):
        assert LabelStudio(
            "http://label-studio",
            "personal-secret",
        ).project_titles() == {"personal-ok"}
    assert len(personal_calls) == 3


def validate_midpoint_projects() -> None:
    for annotator in ANNOTATORS:
        rows = plan_rows(annotator, "MIDPOINT")
        assert {row["task"] for row in rows} == {"MASK", "PRESENCE", "QUALITY"}
        assert {row["image_count"] for row in rows} == {"12"}
        assert all(
            row["project_name"].startswith(f"CB-{annotator}-MID-") for row in rows
        )


def records(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def csv_records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def validate_annotation_release() -> None:
    manifest_path = ROOT / "metadata" / "frames_sampled.csv"
    if not manifest_path.exists():
        return

    manifest = csv_records(manifest_path)
    assert len(manifest) == 377
    images = {row["image"] for row in manifest}
    assert len(images) == len(manifest)
    assert Counter(row["phase"] for row in manifest) == {
        "Launching": 68,
        "Floating": 309,
    }
    assert Counter(row["split"] for row in manifest) == {
        "train": 263,
        "validation": 68,
        "test": 46,
    }

    split_rows = csv_records(ROOT / "splits" / "splits.csv")
    split_map = {row["image"]: row["split"] for row in split_rows}
    assert split_map == {row["image"]: row["split"] for row in manifest}

    frame_files = sorted((ROOT / "frames").glob("*/*.jpg"))
    assert len(frame_files) == len(manifest)
    assert {path.name for path in frame_files} == images
    for path in frame_files:
        assert path.read_bytes()[:3] == b"\xff\xd8\xff", f"Not a JPEG: {path}"
    checksum_rows = {}
    for line in (
        (ROOT / "metadata" / "frame_checksums.sha256")
        .read_text(encoding="utf-8")
        .splitlines()
    ):
        digest, relative = line.split("  ", 1)
        checksum_rows[relative] = digest
    assert len(checksum_rows) == len(frame_files)
    for path in frame_files:
        relative = path.relative_to(ROOT).as_posix()
        assert checksum_rows[relative] == hashlib.sha256(path.read_bytes()).hexdigest()

    assignment_root = ROOT / "annotation" / "assignments"
    calibration = csv_records(assignment_root / "shared_calibration_30.csv")
    qualification = csv_records(assignment_root / "qualification_candidates_12.csv")
    calibration_images = {row["image"] for row in calibration}
    qualification_images = {row["image"] for row in qualification}
    assert len(calibration_images) == 30
    assert len(qualification_images) == 12
    assert not calibration_images & qualification_images

    roster = csv_records(ROOT / "annotation" / "annotator_roster.csv")
    assert tuple(row["annotator_id"] for row in roster) == ANNOTATORS
    assert tuple(row["coauthor_name"] for row in roster) == (
        "Atharva",
        "Pranav G.",
        "Kunsh",
        "Prabhav",
    )
    assert {row["qualification_status"] for row in roster} == {"waived_by_lead"}

    assigned_count: Counter[str] = Counter()
    production_loads: list[int] = []
    for annotator in ANNOTATORS:
        rows = csv_records(assignment_root / f"{annotator}_production.csv")
        production_images = {row["image"] for row in rows}
        assert len(production_images) == len(rows)
        assert not production_images & calibration_images
        assert not production_images & qualification_images
        assert all(row["assignment_type"] == "production" for row in rows)
        assigned_count.update(production_images)
        production_loads.append(len(rows))
    ordinary_images = images - calibration_images - qualification_images
    assert set(assigned_count) == ordinary_images
    assert set(assigned_count.values()) == {2}
    assert max(production_loads) - min(production_loads) <= 1

    segment_rows = csv_records(assignment_root / "segment_assignments.csv")
    assert len(segment_rows) == 68
    assert all(
        row["annotator_1"] in ANNOTATORS
        and row["annotator_2"] in ANNOTATORS
        and row["annotator_1"] != row["annotator_2"]
        for row in segment_rows
    )
    assert sum(int(row["production_frame_count"]) for row in segment_rows) == 335
    assert sum(int(row["calibration_frame_count"]) for row in segment_rows) == 30
    assert sum(int(row["qualification_frame_count"]) for row in segment_rows) == 12

    task_root = ROOT / "label-studio" / "tasks"
    all_tasks = json.loads(
        (task_root / "all_frames_377.json").read_text(encoding="utf-8")
    )
    assert len(all_tasks) == 377
    task_images: set[str] = set()
    for item in all_tasks:
        image = item["meta"]["image"]
        url = item["data"]["image"]
        assert IMAGE.fullmatch(image)
        assert url.startswith(
            "https://raw.githubusercontent.com/ZShamsi987/canyonbench-data/main/frames/"
        )
        assert Path(urlparse(url).path).name == image
        task_images.add(image)
    assert task_images == images

    assert (
        len(
            json.loads(
                (task_root / "shared_calibration_30.json").read_text(encoding="utf-8")
            )
        )
        == 30
    )
    assert (
        len(
            json.loads(
                (task_root / "qualification_12.json").read_text(encoding="utf-8")
            )
        )
        == 12
    )
    for annotator, expected in zip(
        ANNOTATORS,
        production_loads,
        strict=True,
    ):
        tasks = json.loads(
            (task_root / f"{annotator}_production.json").read_text(encoding="utf-8")
        )
        assert len(tasks) == expected

    workload = csv_records(assignment_root / "workload_summary.csv")
    assert len(workload) == 4
    assert {int(row["total_unique_frames"]) for row in workload} == {209, 210}
    assert {int(row["total_submissions"]) for row in workload} == {627, 630}

    project_plan = csv_records(ROOT / "label-studio" / "project_plan.csv")
    assert len(project_plan) == 36
    assert {
        (row["annotator_id"], row["stage"], row["task"]) for row in project_plan
    } == {
        (annotator, stage, task)
        for annotator in ANNOTATORS
        for stage in ("QUALIFICATION", "CALIBRATION", "PRODUCTION")
        for task in ("MASK", "PRESENCE", "QUALITY")
    }
    assert {
        row["start_after"] for row in project_plan if row["stage"] == "QUALIFICATION"
    } == {"waived for current team; do not create"}
    assert {
        row["start_after"] for row in project_plan if row["stage"] == "CALIBRATION"
    } == {"qualification waived by Zafir; start here"}


def main() -> None:
    validate_label_studio_authentication()
    validate_midpoint_projects()
    presence = records(ROOT / "examples/labels/presence.jsonl")
    quality = records(ROOT / "examples/labels/quality.jsonl")
    grids = records(ROOT / "examples/labels/grid.jsonl")
    judges = records(ROOT / "examples/labels/judge_validation.jsonl")
    assert presence and quality and grids and judges
    for record in presence:
        assert IMAGE.fullmatch(str(record["image"]))
        assert all(
            record[feature] in {"yes", "no", "uncertain"} for feature in FEATURES
        )
    expected_cells = {f"{row},{column}" for row in range(4) for column in range(4)}
    for record in grids:
        assert set(record["cells"]) == expected_cells
        assert all(isinstance(value, bool) for value in record["cells"].values())
    for record in judges:
        assert all(
            record["asserts"][feature] in {"yes", "no", "hedged"}
            for feature in FEATURES
        )
    for record in quality:
        assert IMAGE.fullmatch(str(record["image"]))
    schema_examples = {
        "presence.schema.json": presence,
        "quality.schema.json": quality,
        "grid.schema.json": grids,
        "judge_validation.schema.json": judges,
    }
    for schema_name, example_records in schema_examples.items():
        schema = json.loads(
            (ROOT / "schemas" / schema_name).read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for record in example_records:
            validator.validate(record)
    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        Draft202012Validator.check_schema(
            json.loads(schema_path.read_text(encoding="utf-8"))
        )
    for project_path in (ROOT / "label-studio").glob("*.xml"):
        ET.parse(project_path)
    mask_config = ET.parse(ROOT / "label-studio" / "vegetation-mask.xml")
    uncertainty = mask_config.find(".//Choices[@name='uncertain_region']")
    assert uncertainty is not None
    assert uncertainty.get("required") == "true"
    annotator_readme = ROOT / "annotation" / "README.md"
    assert annotator_readme.is_file()
    readme_text = annotator_readme.read_text(encoding="utf-8")
    for required_section in (
        "exact team and current plan",
        "Shared Google Drive submission folder",
        "Mac installation",
        "Windows installation",
        "create your calibration projects",
        "Sammy only",
        "Exact daily annotation loop",
        "how to label vegetation masks",
        "how to label feature presence",
        "how to label image quality",
        "pausing and resuming safely",
        "exact export and Google Drive upload procedure",
        "Troubleshooting",
    ):
        assert required_section.casefold() in readme_text.casefold()
    validate_annotation_release()
    print("All example contracts passed")


if __name__ == "__main__":
    main()
