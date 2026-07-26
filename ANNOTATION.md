# Annotation quick reference

The full CanyonBench Annotation Manual is authoritative. This page routes files and checks; it does not replace the numbered rules.

## Production workflow

1. Build the private handoff with `scripts/prepare_curation_package.py`, then have the lead adjudicate gold labels for the 12 qualification candidates.
2. Set a stable annotator id. Complete the 12-frame qualification set and meet the agreement targets.
3. Label assigned whole trajectory segments plus the shared 30-frame calibration set.
4. At 100% zoom, pan left-to-right and top-to-bottom. Mark unresolved cases `uncertain` and add them to `metadata/decision_log.csv`.
5. Create the vegetation mask first, then presence and quality. Registration points are placed separately and checked by a second coauthor.
6. Compute the 4x4 grid from the final mask only for reliable registrations; review the overlay and log any override.
7. Keep per-annotator files. The lead creates adjudicated records without overwriting source passes.

## Build the private handoff

From the data repository:

```bash
python scripts/prepare_curation_package.py \
  /path/to/work/world10/frames_sampled.csv \
  /path/to/work/world10/frames_named \
  private/curation/world10 \
  splits/splits.csv
```

The private output contains hardlinked phase directories, Label Studio tasks,
registration candidates, the shared calibration set, qualification candidates,
and a two-annotator segment assignment sheet. It is ignored by Git.

## Visible green vegetation

Include resolvable green, olive-green, or dark-green living vegetation. Exclude tan/dry grass, water or algae ambiguity, mineral tint, unconfirmed shadow, diffuse sub-resolution green tint, and connected specks under four pixels. Trace the >50% pixel boundary and do not pad segmenter proposals.

## Feature minimums

- water: contiguous ~20-pixel region that visibly reads as water;
- road/trail: linear feature with at least two engineered cues;
- building/structure: regular man-made geometry;
- dense forest: continuous canopy larger than roughly one 4x4 cell;
- snow/ice: soft conforming white cover, distinct from rock/cloud;
- cultivated field: geometric agricultural parcels.

Some evidence below a minimum is `uncertain`, not `no`. Natural erosion lines with no engineered cues are `no` for road. Never infer one feature from another.

## Output paths

```text
masks/annotator/img_SSSSSS__ID.png
masks/adjudicated/img_SSSSSS.png
labels/annotator/presence.jsonl
labels/annotator/quality.jsonl
labels/annotator/grid.jsonl
labels/annotator/judge_validation.jsonl
labels/adjudicated/presence.jsonl
labels/adjudicated/quality.jsonl
labels/adjudicated/grid.jsonl
registration/points/img_SSSSSS.points
registration/residuals.csv
```
