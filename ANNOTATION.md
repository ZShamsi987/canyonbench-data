# Annotation quick reference

The full CanyonBench Annotation Manual is authoritative. This page routes files and checks; it does not replace the numbered rules.

## Start here

New annotators use
[`annotation/README.md`](annotation/README.md), which assumes no GitHub, Python,
Docker, or Label Studio experience. The project lead uses
[`docs/START_ANNOTATING.md`](docs/START_ANNOTATING.md). The public task files
load the 377 curated JPEGs directly from GitHub; annotators do not need the raw
Google Drive footage.

## Production workflow

1. Keep the fixed mapping in `annotation/annotator_roster.csv`: Atharva=`A1`,
   Pranav G.=`A2`, Kunsh=`A3`, and Prabhav=`A4`.
2. Sammy creates private gold/reference labels for the 12 qualification
   candidates and keeps them hidden until production exports are locked.
3. Qualification is waived for this previously tested A1-A4 team; everyone
   starts with calibration.
4. All four label the shared 30-frame calibration set, upload the first-five
   checkpoint to their own shared-Drive folders, and resolve ambiguities in a
   lead-run meeting.
   and resolve ambiguities through the append-only decision log.
5. Create the production projects from the fixed per-annotator worklist.
6. At 100% zoom, pan left-to-right and top-to-bottom. Mark unresolved cases
   `uncertain` and add them to `metadata/decision_log.csv`.
7. Create the vegetation mask first, then presence and quality. Registration
   begins only after the reference product and license are recorded.
8. Keep per-annotator exports. The lead creates adjudicated records without
   overwriting source passes.

## Create projects automatically

After starting a local Label Studio instance and copying its API key:

```bash
export LABEL_STUDIO_API_KEY='paste-token'
python3 scripts/create_label_studio_projects.py --lead-gold

# Each coauthor runs this with their own id:
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage CALIBRATION
unset LABEL_STUDIO_API_KEY
```

The lead authorizes `PRODUCTION` after reviewing calibration. At 84 completed
tasks per production project, each annotator runs `--stage MIDPOINT`, uploads
the four midpoint exports, and waits for authorization to resume. The reusable
36-project plan remains in `label-studio/project_plan.csv`.

## Rebuild the public handoff

The published files are reproducible from the code repository's sampled
manifest and named-frame directory:

```bash
python3 scripts/prepare_annotation_release.py \
  /path/to/work/world10/frames_sampled.csv \
  /path/to/work/world10/frames_named \
  --output .
```

This materializes 377 curated JPEGs, deterministic A1-A4 assignments, task
JSON, workload summaries, and the pre-annotation metadata manifest.

The older ignored local handoff can still be rebuilt for audit:

```bash
python3 scripts/prepare_curation_package.py \
  /path/to/work/world10/frames_sampled.csv \
  /path/to/work/world10/frames_named \
  private/curation/world10 \
  splits/splits.csv
```

Its local-file URLs are for offline audit only. Annotators use the public files
under `label-studio/tasks/`.

## Annotator workload

- A1 and A4: 168 production + 30 calibration + 12 midpoint images.
- A2 and A3: 167 production + 30 calibration + 12 midpoint images.
- Every ordinary production image has exactly two independent annotators.
- Calibration and midpoint images are labeled by all four.
- Each image is completed in the mask, presence, and quality projects.

## Task order

1. Sammy's private gold/reference set
2. Calibration checkpoint and final
3. Production first half
4. Midpoint repeat
5. Production final
6. Adjudication
7. Lead-assigned registration and grounding with the frozen 2023 USGS NAIP source

Do not skip a gate.

## Visible green vegetation

Label from `frames_corrected/` only (A-13). Include resolvable living vegetation
where **green is the dominant channel** judged in isolation, not merely darker or
greyer than its surroundings (A-14, A-15). Exclude tan/dry grass, water or algae
ambiguity, mineral tint, darker brown rock units, canyon shadow, diffuse
sub-resolution green tint, and connected specks under four pixels. Trace the
>50% pixel boundary and do not pad segmenter proposals.

Haze hides vegetation and never creates it: mask only what is visible and record
the haze in `clarity` (A-16). Expect small masks — median cover is 0.009% of a
frame and the maximum anywhere in the sampled set is 2.4% (A-17).

## Feature minimums

- water: contiguous ~20-pixel region that visibly reads as water;
- road/trail: linear feature with at least two engineered cues;
- building/structure: regular man-made geometry;
- dense forest: continuous canopy larger than roughly one 4x4 cell;
- snow/ice: soft conforming white cover, distinct from rock/cloud;
- cultivated field: geometric agricultural parcels.

Some evidence below a minimum is `uncertain`, not `no`. Natural erosion lines
with no engineered cues are `no` for road. Never infer one feature from another.

## Output paths

```text
masks/annotator/img_SSSSSS__ID.png
masks/adjudicated/img_SSSSSS.png
labels/annotator/ID_presence.jsonl
labels/annotator/ID_quality.jsonl
labels/annotator/ID_grid.jsonl
labels/annotator/ID_judge_validation.jsonl
labels/adjudicated/presence.jsonl
labels/adjudicated/quality.jsonl
labels/adjudicated/grid.jsonl
registration/points/img_SSSSSS.points
registration/residuals.csv
```
