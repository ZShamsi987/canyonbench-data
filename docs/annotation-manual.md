# CanyonBench Annotation Manual

Operational rules accompanying project specification revision 2. Cite rule ids when resolving disagreements. Anything not determined here is marked uncertain and entered in the append-only decision log; the adjudicated ruling becomes a new numbered rule.

## General rules

- **G-1** Label only what is visible in the cropped frame. Never use knowledge of the region or flight path.
- **G-2** Work at 100% (1:1) zoom for masks/control points and pan left-to-right, top-to-bottom.
- **G-3** If a rule does not fully determine the decision, choose `uncertain`, do not guess, and log it.
- **G-4** Do not silently revise earlier labels after a later realization. Log the insight for uniform adjudication.
- **G-5** Key every image output exactly to `img_SSSSSS.jpg`.

## Tools and setup

- **T-1** Use one Label Studio project per task. Masks use a Segment Anything click-to-segment backend on an Adroit GPU.
- **T-2** Place control points in QGIS Georeferencer with the frame as source
  and the frozen 2023 USGS NAIP ImageServer as target. Set the project and
  target CRS to `EPSG:26912`; follow `docs/registration.md`.
- **T-3** Export masks as same-size, single-channel 8-bit PNGs: 255 vegetation, 0 background.
- **T-4** Use one stable annotator id in every record and filename.

## Task A: vegetation masks

The target is living green vegetation visible in the frame.

- **A-1** Include only green, olive-green, or dark-green regions. Tan, brown, gray, red, and white are not vegetation.
- **A-2** Exclude dry, brown, or straw-colored grass even if it is a plant; RGB cannot distinguish it from dead material reliably.
- **A-3** If a green region could be water, algae film, or green mineral, exclude it and set the uncertainty/clarity flag.
- **A-4** Include vegetation in shadow only when its identity remains confirmable.
- **A-5** Minimum region size is four connected pixels at 100% zoom. Exclude isolated one-to-three-pixel noise.
- **A-6** Exclude diffuse sub-resolution green tint that cannot be resolved into patches at 100%.
- **A-7** A boundary pixel is vegetation when more than half of the pixel is vegetation. Trace the edge; do not dilate or pad.
- **A-8** Always exclude cloud, haze, snow, water, shadow, rock, sand, and man-made surfaces.
- **A-9** At 100% from the top-left, click inside each patch for a segmenter proposal; correct overrun/omission with a small brush/eraser.
- **A-10** Repeat in G-2 order and export `masks/annotator/img_SSSSSS__ID.png`.

Examples: include a resolvable dark-green ribbon on a river bank; exclude tan plateau grassland; exclude a faint unresolved green wash.

## Task B: feature presence

For every feature choose `yes`, `no`, or `uncertain`.

- **B-0** Use `uncertain` for nonzero evidence below the minimum or whenever the answer depends on interpretation.
- **B-1 Water** `yes` requires a contiguous region of roughly 20 pixels that reads as water through smooth texture, water color, or specular sheen, and lies in a channel/basin rather than a shaded slope.
- **B-2 Road/trail** `yes` requires at least two engineered cues: consistent width along length; hard/straight or smoothly curved edges; a cut or embankment across terrain; visible junction or vehicle; connection to structures. Exactly one cue is `uncertain`; zero is natural/`no`.
- **B-3 Building/structure** `yes` requires regular man-made geometry such as straight edges, right angles, rooftops, a dam, or a tower.
- **B-4 Dense forest** `yes` requires continuous tree canopy over a contiguous area larger than roughly one 4x4 cell; scattered shrubs do not count.
- **B-5 Snow/ice** `yes` requires white cover with a soft conforming snow shape, not hard-edged bright rock or wispy cloud.
- **B-6 Cultivated field** `yes` requires geometric agricultural parcels, regular boundaries, or a center-pivot circle.
- **B-7** A dry wash, ridgeline, or natural erosion line with zero engineered cues is `no` for road regardless of resemblance.
- **B-8** Never infer one feature from another. Judge each from its own visible evidence.

## Task C: registration control points

- **C-0** Stream the official source recorded in
  `registration/reference/source.yaml`. Do not download the 189 full source
  tiles or use an unrecorded basemap.
- **C-1** Place at least six pairs and aim for eight: at least one per quadrant and one near the center. Do not cluster or make them collinear.
- **C-2** Use point-like, unambiguous, temporally stable landmarks: confluences/sharp bends, road junctions, building corners, distinctive rock spires/notches, or stable shoreline points.
- **C-3** Do not use shadow edges, moving water lines/shorelines, cloud edges, vehicles, or ambiguous smooth curves.
- **C-4** Set QGIS transformation to Projective. Mark at least two points as held-out checks, fit without them, and measure their reprojection error.
- **C-5** Reliability requires held-out error no greater than one quarter of a grid-cell ground width. If not, or if six good points do not exist, set registration to none and exclude the frame from Task D.
- **C-6** Export `registration/points/img_SSSSSS.points` and append counts, held-out RMSE in metres, threshold, and reliability to `registration/residuals.csv`.

## Task D: grounding grid

- **D-1** For a reliable frame only, a 4x4 cell is positive when at least 1% of its pixels are vegetation in the final mask.
- **D-2** Review the computed overlay. Override only when the mask is visibly wrong in that cell, and log the override.
- **D-3** Skip frames whose registration is none/unreliable.

Rows and columns are zero-indexed from the top-left and keys are `0,0` through `3,3`.

## Task E: quality and condition

- `cloud`: `none` when cloud/haze covers under 5% of ground; `partial` at 5-33%; `heavy` above 33%.
- `clarity`: `clear` when ground texture/shadows are crisp; `moderate` when contrast is reduced but features remain identifiable; `heavy` when ground is washed out and colors muted.
- `balloon`: `none` when no balloon pixel remains after the left crop; `partial` when any envelope is visible.
- `sharpness`: `sharp` for crisp edges at 100%; `blurred` for directional edge smear.
- `exposure`: `ok`; `over` when clipped white highlights cover over 10%; `under` when crushed detail-losing shadows cover over 10%.
- `glare`: `none`; `present` for visible bright bloom or veiling flare.
- **E-1** Heavy cloud, heavy clarity loss, or partial balloon makes a frame an exclusion candidate. Record the keep/drop decision and reason in the master table.

## Task F: caption-judge validation

- **F-1** From caption text alone, mark a feature `yes` when explicitly/unambiguously asserted, `no` when absent or negated, and `hedged` when qualified.
- **F-2** Use only the six-feature ontology, do not open the image, and hide the evaluated model identity.

## Assignment and adjudication

- **W-1** Two coauthors independently label masks, presence, and quality. One places control points and a second checks a shared subset.
- **W-2** Assign whole contiguous segments, plus a shared 30-frame calibration subset labeled by all annotators.
- **W-3** Each annotator normally passes the 12-frame gold qualification set
  before production. The lead may document an equivalent prior test and an
  explicit waiver in `annotation/annotator_roster.csv` before calibration.
  Zafir recorded that waiver for A1-A4 on 2026-07-26; the midpoint repeat
  remains mandatory.
- **W-4** Preserve `img_SSSSSS__ID.png`; the adjudicated final is `img_SSSSSS.png`.
- **Q-1** Put unresolved cases in the append-only log with frame, question, consulted rules, ruling, and new numbered rule. Apply it retrospectively during adjudication.
- **Q-2** Hold a short weekly adjudication, finalize conflicts, and fold rulings into the manual.
- **Q-3** Repeat the qualification set midway; re-align any drift before production continues.

Targets: mask Dice at least 0.75; presence and quality Cohen/Fleiss kappa at least 0.6; control-point errors consistently below threshold. The lead finalizes mask conflicts; categorical ties require group adjudication; caption-judge pairwise agreement is reported but not gated.

## Exact records

```json
{"image":"img_006806.jpg","annotator":"ZH","water":"yes","road":"no","building":"no","forest":"no","snow":"no","field":"uncertain"}
```

```json
{"image":"img_006806.jpg","annotator":"ZH","cloud":"none","clarity":"clear","balloon":"none","sharpness":"sharp","exposure":"ok","glare":"none"}
```

```json
{"image":"img_006806.jpg","annotator":"ZH","cells":{"0,0":true,"0,1":false,"0,2":false,"0,3":false,"1,0":false,"1,1":false,"1,2":false,"1,3":false,"2,0":false,"2,1":false,"2,2":false,"2,3":false,"3,0":false,"3,1":false,"3,2":false,"3,3":false}}
```

```json
{"caption_id":"c0007","annotator":"ZH","asserts":{"water":"yes","road":"hedged","building":"no","forest":"no","snow":"no","field":"no"}}
```

Machine-readable definitions in `schemas/` are the release contract.
