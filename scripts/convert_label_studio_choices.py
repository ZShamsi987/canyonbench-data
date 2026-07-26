#!/usr/bin/env python3
"""Convert Label Studio presence or quality exports to CanyonBench JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

FIELDS = {
    "presence": ("water", "road", "building", "forest", "snow", "field"),
    "quality": (
        "cloud",
        "clarity",
        "balloon",
        "sharpness",
        "exposure",
        "glare",
    ),
}


def image_key(task: dict[str, Any]) -> str:
    meta = task.get("meta") or {}
    if meta.get("image"):
        return str(meta["image"])
    return Path(urlparse(task["data"]["image"]).path).name


def annotation_results(task: dict[str, Any]) -> list[dict[str, Any]]:
    annotations = [
        annotation
        for annotation in task.get("annotations", [])
        if not annotation.get("was_cancelled", False)
    ]
    if len(annotations) != 1:
        raise ValueError(
            f"{image_key(task)} has {len(annotations)} completed annotations; "
            "each per-annotator project must have exactly one"
        )
    return annotations[0].get("result", [])


def convert_task(
    task: dict[str, Any],
    task_type: str,
    annotator: str,
) -> dict[str, str]:
    expected = FIELDS[task_type]
    choices: dict[str, str] = {}
    for result in annotation_results(task):
        from_name = result.get("from_name")
        values = result.get("value", {}).get("choices", [])
        if from_name in expected:
            if len(values) != 1:
                raise ValueError(
                    f"{image_key(task)} field {from_name} does not have one choice"
                )
            choices[str(from_name)] = str(values[0])
    missing = set(expected) - set(choices)
    if missing:
        raise ValueError(
            f"{image_key(task)} is missing {task_type} fields: {sorted(missing)}"
        )
    return {
        "image": image_key(task),
        "annotator": annotator,
        **{field: choices[field] for field in expected},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exports", nargs="+", type=Path)
    parser.add_argument("--task", required=True, choices=tuple(FIELDS))
    parser.add_argument("--annotator", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    converted: list[dict[str, str]] = []
    for path in args.exports:
        tasks = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(tasks, list):
            raise ValueError(f"{path} is not a Label Studio task list")
        converted.extend(
            convert_task(task, args.task, args.annotator) for task in tasks
        )
    images = [record["image"] for record in converted]
    if len(set(images)) != len(images):
        raise ValueError("The supplied exports contain duplicate image annotations")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as stream:
        for record in sorted(converted, key=lambda item: item["image"]):
            stream.write(json.dumps(record, separators=(",", ":")) + "\n")
    print(f"Wrote {len(converted)} {args.task} records to {args.output}")


if __name__ == "__main__":
    main()
