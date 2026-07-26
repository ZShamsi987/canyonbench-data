#!/usr/bin/env python3
"""Create one gated CanyonBench Label Studio stage for one annotator."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALID_ANNOTATORS = ("A1", "A2", "A3", "A4")
VALID_STAGES = ("QUALIFICATION", "CALIBRATION", "PRODUCTION", "MIDPOINT")
ANNOTATOR_NAMES = {
    "A1": "Atharva",
    "A2": "Pranav G.",
    "A3": "Kunsh",
    "A4": "Prabhav",
    "LEAD": "Sammy",
}


class LabelStudio:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.authorization = f"Token {api_key}"
        self.personal_token_checked = False

    def _send(
        self,
        method: str,
        path: str,
        payload: object | None = None,
        authorization: str | None = None,
    ) -> Any:
        body = None
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        if payload is not None:
            body = json.dumps(payload).encode()
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
        return json.loads(content) if content else None

    def _activate_personal_access_token(self) -> bool:
        """Exchange a Label Studio PAT for a short-lived bearer token."""
        if self.personal_token_checked:
            return False
        self.personal_token_checked = True
        try:
            response = self._send(
                "POST",
                "/api/token/refresh",
                {"refresh": self.api_key},
            )
        except (urllib.error.HTTPError, urllib.error.URLError):
            return False
        if not isinstance(response, dict) or not response.get("access"):
            return False
        self.authorization = f"Bearer {response['access']}"
        return True

    def request(
        self,
        method: str,
        path: str,
        payload: object | None = None,
    ) -> Any:
        try:
            return self._send(method, path, payload, self.authorization)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            if error.code in (401, 403) and self._activate_personal_access_token():
                try:
                    return self._send(method, path, payload, self.authorization)
                except urllib.error.HTTPError as retry_error:
                    retry_detail = retry_error.read().decode(errors="replace")
                    raise RuntimeError(
                        "Label Studio returned HTTP "
                        f"{retry_error.code} for {path}: {retry_detail}"
                    ) from retry_error
                except urllib.error.URLError as retry_error:
                    raise RuntimeError(
                        f"Cannot reach Label Studio at {self.base_url}: "
                        f"{retry_error.reason}"
                    ) from retry_error
            raise RuntimeError(
                f"Label Studio returned HTTP {error.code} for {path}: {detail}"
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError(
                f"Cannot reach Label Studio at {self.base_url}: {error.reason}"
            ) from error

    def project_titles(self) -> set[str]:
        response = self.request("GET", "/api/projects/?page_size=100")
        projects = (
            response.get("results", response)
            if isinstance(response, dict)
            else response
        )
        return {str(project["title"]) for project in projects}

    def create_project(
        self,
        title: str,
        label_config: str,
        description: str,
    ) -> int:
        response = self.request(
            "POST",
            "/api/projects/",
            {
                "title": title,
                "description": description,
                "label_config": label_config,
                "maximum_annotations": 1,
                "is_published": True,
            },
        )
        return int(response["id"])

    def import_tasks(self, project_id: int, tasks: list[dict[str, Any]]) -> Any:
        return self.request(
            "POST",
            f"/api/projects/{project_id}/import",
            tasks,
        )


def plan_rows(annotator: str, stage: str) -> list[dict[str, str]]:
    with (ROOT / "label-studio" / "project_plan.csv").open(
        newline="",
        encoding="utf-8",
    ) as stream:
        rows = list(csv.DictReader(stream))
    source_stage = "QUALIFICATION" if stage == "MIDPOINT" else stage
    selected = [
        row
        for row in rows
        if row["annotator_id"] == annotator and row["stage"] == source_stage
    ]
    if stage == "MIDPOINT":
        selected = [
            {
                **row,
                "stage": "MIDPOINT",
                "project_name": row["project_name"].replace("-QUAL-", "-MID-"),
                "start_after": "lead pauses production for the midpoint repeat",
            }
            for row in selected
        ]
    if len(selected) != 3:
        raise ValueError(
            f"Expected three {stage} projects for {annotator}, found {len(selected)}"
        )
    return selected


def lead_gold_rows() -> list[dict[str, str]]:
    rows = plan_rows("A1", "QUALIFICATION")
    return [
        {
            **row,
            "annotator_id": "LEAD",
            "stage": "LEAD_GOLD",
            "project_name": row["project_name"].replace(
                "CB-A1-QUAL-",
                "CB-LEAD-GOLD-",
            ),
            "start_after": "none; complete before coauthor scoring",
        }
        for row in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create the mask, presence, and quality projects for one gated stage"
        )
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--annotator", choices=VALID_ANNOTATORS)
    target.add_argument(
        "--lead-gold",
        action="store_true",
        help="Create the lead's three private 12-frame gold projects",
    )
    parser.add_argument(
        "--stage",
        type=str.upper,
        choices=VALID_STAGES,
    )
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument(
        "--api-key-env",
        default="LABEL_STUDIO_API_KEY",
        help="Environment variable containing the Label Studio API key",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the projects without calling Label Studio",
    )
    parser.add_argument(
        "--allow-waived-qualification",
        action="store_true",
        help=(
            "Override the current A1-A4 qualification waiver. "
            "Do not use during the July-August 2026 annotation sprint."
        ),
    )
    args = parser.parse_args()

    if args.lead_gold:
        if args.stage:
            parser.error("--lead-gold cannot be combined with --stage")
        annotator = "LEAD"
        stage = "LEAD_GOLD"
        rows = lead_gold_rows()
    else:
        if not args.stage:
            parser.error("--stage is required with --annotator")
        if args.stage == "QUALIFICATION" and not args.allow_waived_qualification:
            parser.error(
                "Qualification is waived for the current A1-A4 team. "
                "Start with --stage CALIBRATION. Use "
                "--allow-waived-qualification only if the project lead "
                "explicitly reinstates the gate."
            )
        annotator = args.annotator
        stage = args.stage
        rows = plan_rows(annotator, stage)

    if args.dry_run:
        for row in rows:
            print(
                f"{row['project_name']}: {row['image_count']} images, "
                f"{row['label_config']}, {row['task_file']}"
            )
        return

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(
            f"Set {args.api_key_env} to the token from Label Studio "
            "Account & Settings, then run this command again."
        )
    client = LabelStudio(args.url, api_key)
    existing = client.project_titles()

    created = 0
    for row in rows:
        title = row["project_name"]
        if title in existing:
            print(f"SKIP existing project: {title}", file=sys.stderr)
            continue
        label_config = (ROOT / row["label_config"]).read_text(encoding="utf-8")
        tasks = json.loads((ROOT / row["task_file"]).read_text(encoding="utf-8"))
        expected = int(row["image_count"])
        if len(tasks) != expected:
            raise ValueError(
                f"{row['task_file']} has {len(tasks)} tasks; expected {expected}"
            )
        person = ANNOTATOR_NAMES[annotator]
        description = (
            f"CanyonBench {stage.lower()} {row['task'].lower()} work "
            f"for {annotator} ({person}). Follow annotation/README.md and "
            "docs/annotation-manual.md. Do not view another coauthor's work."
        )
        project_id = client.create_project(title, label_config, description)
        response = client.import_tasks(project_id, tasks)
        imported = response.get("task_count") if isinstance(response, dict) else None
        if imported is not None and int(imported) != expected:
            raise RuntimeError(
                f"{title} imported {imported} tasks; expected {expected}"
            )
        print(
            f"CREATED {title}: {expected} tasks at "
            f"{args.url.rstrip('/')}/projects/{project_id}"
        )
        created += 1

    print(f"Created {created} project(s) for {annotator} {stage}.")


if __name__ == "__main__":
    main()
