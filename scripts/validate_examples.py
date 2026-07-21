#!/usr/bin/env python3
"""Validate checked-in example JSONL records with only the standard library."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
IMAGE = re.compile(r"^img_\d{6,}\.jpg$")
FEATURES = ("water", "road", "building", "forest", "snow", "field")


def records(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    presence = records(ROOT / "examples/labels/presence.jsonl")
    quality = records(ROOT / "examples/labels/quality.jsonl")
    grids = records(ROOT / "examples/labels/grid.jsonl")
    judges = records(ROOT / "examples/labels/judge_validation.jsonl")
    assert presence and quality and grids and judges
    for record in presence:
        assert IMAGE.fullmatch(str(record["image"]))
        assert all(record[feature] in {"yes", "no", "uncertain"} for feature in FEATURES)
    expected_cells = {f"{row},{column}" for row in range(4) for column in range(4)}
    for record in grids:
        assert set(record["cells"]) == expected_cells
        assert all(isinstance(value, bool) for value in record["cells"].values())
    for record in judges:
        assert all(record["asserts"][feature] in {"yes", "no", "hedged"} for feature in FEATURES)
    for record in quality:
        assert IMAGE.fullmatch(str(record["image"]))
    schema_examples = {
        "presence.schema.json": presence,
        "quality.schema.json": quality,
        "grid.schema.json": grids,
        "judge_validation.schema.json": judges,
    }
    for schema_name, example_records in schema_examples.items():
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for record in example_records:
            validator.validate(record)
    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))
    for project_path in (ROOT / "label-studio").glob("*.xml"):
        ET.parse(project_path)
    print("All example contracts passed")


if __name__ == "__main__":
    main()
