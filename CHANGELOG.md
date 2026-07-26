# Changelog

## Unreleased

- Entered private-source curation without committing raw telemetry, thermal logs, or footage.
- Recorded source-log checksums, the 406-clip inventory count, invalid absolute
  camera-clock status, verified relative clip timing, and the release/ascent
  synchronization anchor.
- Kept the MLX thermal log explicitly excluded from benchmark inputs.
- Added a reproducible private curation-package builder for sampled frames, Label Studio tasks, calibration and qualification candidates, registration candidates, and two-annotator segment assignments.
- Published the 377-frame annotation set after the capture owner confirmed
  redistribution rights for the annotation handoff.
- Added deterministic balanced A1-A4 segment assignments: 335 ordinary frames
  receive two passes, while 30 calibration and 12 qualification frames go to
  all four coauthors.
- Added public-URL Label Studio tasks, a 36-project gated plan, automatic local
  project creation, categorical-export conversion, checksums, and comprehensive
  lead/annotator instructions.
- Added a first-time annotator README with no-account ZIP download, separate
  macOS and Windows setup, per-task decisions, exports, pause/resume, stage
  gates, and troubleshooting.
- Locked the current sprint roster (Sammy gold; Atharva A1; Pranav G. A2;
  Kunsh A3; Prabhav A4), documented the qualification waiver, shared-Drive
  handoff, four-to-five-day annotation sprint, and August 20 freeze target.
- Kept raw footage, flight logs, reference imagery, qualification gold answers,
  and raw annotation exports out of the public repository.

## 0.1.0-predata - 2026-07-21

- Added complete public schemas, annotation project templates, metadata contracts, provenance placeholders, example records, and validation checks.
- No real flight data or annotation claims are included in this pre-data release.
