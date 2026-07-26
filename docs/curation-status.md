# World-10 curation status

Automated curation and the public annotation handoff are complete. This record
does not claim that annotation, registration, final license designation, full
release audit, or release validation is complete.

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
- Published all 377 curated Launching/Floating JPEGs without publishing the raw
  footage or private flight logs.
- Published public-URL Label Studio task files, a deterministic balanced A1-A4
  segment assignment, 30-frame shared calibration set, 12-frame qualification
  set, workload audit, and exact project plan.
- Confirmed that ordinary production images have exactly two assignees and that
  each coauthor has 167 or 168 production frames.
- Recorded the capture owner's 2026-07-26 confirmation of redistribution rights
  for the public annotation handoff.
- Recorded raw-log, source-video-manifest, sampled-manifest, configuration, and
  split hashes in `metadata/provenance.yaml`.
- Selected and audited the official 2023 USGS NAIP reference: 189 primary
  Arizona tiles cover the full flight bbox at 0.3 metre nominal resolution.
- Recorded the public-domain terms, requested acknowledgment, exact ImageServer,
  catalog query, metric registration CRS, and remote-first bounded-cache policy.

## Human or external gates remaining

- Complete Sammy's private 12-frame gold answers.
- Complete the shared calibration set and begin production using
  `docs/START_ANNOTATING.md`; A1-A4 qualification is waived after prior testing.
- Complete and document the full-frame frozen-release privacy review.
- Record the final image-data license designation.
- Obtain two independent annotation passes, adjudicate, and report agreement.
- Place and check registration control points; publish held-out metric errors.
- Calibrate VARI only on the designated calibration population.
- Build and validate the frozen release.
- Publish Hugging Face artifacts, Zenodo DOI, and final citation metadata.

No raw telemetry, raw footage, or large reference raster is committed to this
repository. The reproducible USGS service contract is committed, and the 377
derived annotation JPEGs are public.
