# World-10 curation status

Automated curation is complete. This record does not claim that annotation,
registration, licensing, privacy review, or release validation is complete.

## Completed

- Selected the only reset-delimited telemetry segment containing Launching,
  Floating, and Terminating in order; excluded 23 test/power-cycle segments.
- Retained 24,255 valid operational telemetry rows.
- Inventoried 406 source AVI files: 405 decodable and one audited zero-filled
  placeholder (`MOVA0486.avi`).
- Verified the release/ascent anchor at `MOVA0081.avi + 37 s`, corresponding to
  flight elapsed second 2721.
- Preserved relative clip timing while rejecting the camera's invalid absolute
  date.
- Extracted 23,239 cropped one-Hz frames and resolved clip overlaps into 23,062
  unique flight-second names.
- Audited 1,500 image seconds without valid telemetry instead of interpolating.
- Joined 21,216 Launching/Floating frames to telemetry and objective quality
  controls.
- Sampled 377 frames: 68 Launching and 309 Floating.
- Frozen 68 bounded trajectory segments and 67 geographic blocks.
- Frozen splits: 263 train, 68 validation, and 46 test, with zero block or
  segment leakage.
- Built an ignored private handoff with 377 Label Studio tasks, a shared
  30-frame calibration set, 12 qualification candidates, two-annotator segment
  assignments, and 377 registration candidates.
- Recorded raw-log, source-video-manifest, sampled-manifest, configuration, and
  split hashes in `metadata/provenance.yaml`.

## Human or external gates remaining

- Confirm source-video redistribution rights.
- Complete full-frame privacy review.
- Create adjudicated gold answers for the 12 qualification candidates.
- Obtain two independent annotation passes, adjudicate, and report agreement.
- Acquire and document licensed reference imagery.
- Place and check registration control points; publish held-out metric errors.
- Calibrate VARI only on the designated calibration population.
- Build and validate the frozen release.
- Publish approved imagery, Hugging Face artifacts, Zenodo DOI, and final
  citation metadata.

No raw telemetry, raw footage, reference imagery, or private frame file is
committed to this repository.
