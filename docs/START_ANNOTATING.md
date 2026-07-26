# Start annotating CanyonBench

This is the operational handoff for the project lead and the four coauthor
annotators. It is deliberately explicit. The numbered
[annotation manual](annotation-manual.md) remains authoritative whenever this
guide and a labeling decision seem to conflict.

The 377 annotation images are public GitHub files. Nobody needs the 71 GB raw
Google Drive folder, the flight logs, or a repository clone to label them.
Label Studio reads each JPEG directly from the URL embedded in the task file.

## What the project lead must do first

Do these steps in order.

1. Open `annotation/annotator_roster.csv`.
2. Map each coauthor to exactly one permanent id: `A1`, `A2`, `A3`, or `A4`.
   Add the coauthor name and Label Studio email. Never change an id after work
   starts.
3. Create the 12-frame lead-gold qualification projects with the one-command
   setup below, label them, and keep the answers private until every coauthor
   has submitted their qualification pass.
4. Send each coauthor their id and the public URL of this guide.
5. Tell them to create only the three **QUALIFICATION** projects first.
6. Score qualification. Mark `passed` and the date in
   `annotation/annotator_roster.csv` only when all three gates pass.
7. After a pass, authorize the three **CALIBRATION** projects. Review the first
   five images together before anyone continues.
8. After calibration alignment, authorize the three **PRODUCTION** projects.

Do not start registration yet. Visible-image masks, presence, and quality can
proceed now. Registration remains blocked until the reference imagery product
and its redistribution/use terms are recorded.

## Exact workload

Every ordinary production image has one fixed pair of annotators for all three
tasks. The pair owns the whole trajectory segment. Shared calibration and
qualification images are removed from ordinary worklists, so no one labels an
image twice by accident.

| ID | Production | Calibration | Qualification | Unique images | Total submissions |
|---|---:|---:|---:|---:|---:|
| A1 | 168 | 30 | 12 | 210 | 630 |
| A2 | 167 | 30 | 12 | 209 | 627 |
| A3 | 167 | 30 | 12 | 209 | 627 |
| A4 | 168 | 30 | 12 | 210 | 630 |

A submission means one completed mask, presence form, or quality form. Workload
source files are in `annotation/assignments/`. The fixed segment pairs are in
`segment_assignments.csv`; do not rebalance them informally.

## Label Studio: easiest independent setup

Use a separate local Label Studio instance for each coauthor. This prevents
people from seeing one another's annotations and avoids the Community Edition
limitation that specific tasks cannot be assigned to specific annotators.

### 1. Start Label Studio

Install Docker Desktop, open a terminal, and run:

```bash
mkdir -p "$PWD/canyonbench-label-studio"
docker run --name canyonbench-label-studio -it \
  -p 8080:8080 \
  -v "$PWD/canyonbench-label-studio:/label-studio/data" \
  heartexlabs/label-studio:latest
```

Keep that terminal open. Open `http://localhost:8080`, create the local account,
then open **Account & Settings** and copy the API key.

For later sessions, restart the same saved instance with:

```bash
docker start -a canyonbench-label-studio
```

If port 8080 is already occupied, replace both occurrences of `8080` in the
commands and URL with an unused port such as `8081`.

### 2. Obtain the repository

The automated setup script is the least error-prone route:

```bash
git clone https://github.com/ZShamsi987/canyonbench-data.git
cd canyonbench-data
```

This clone is roughly 50 MiB, not 71 GB. It contains only the 377 curated JPEGs
and annotation files.

### 3. Create the three projects for the current stage

On macOS or Linux:

```bash
export LABEL_STUDIO_API_KEY='paste-your-token-here'
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage QUALIFICATION
unset LABEL_STUDIO_API_KEY
```

Replace `A1` with the id assigned by the lead. On Windows PowerShell, use:

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-token-here"
python scripts/create_label_studio_projects.py --annotator A1 --stage QUALIFICATION
Remove-Item Env:LABEL_STUDIO_API_KEY
```

The script creates exactly three projects: mask, presence, and quality. It
imports 12 tasks into each and prints clickable local project URLs. It never
uploads the images because the tasks already contain public image URLs.

After the lead records a qualification pass, run the same command with:

```text
--stage CALIBRATION
```

After the lead reviews calibration, run it once more with:

```text
--stage PRODUCTION
```

Do not create or enter a later stage early. The complete 36-project audit plan
is in `label-studio/project_plan.csv`.

### Lead-only gold project command

The project lead uses the same local setup and API key, then runs:

```bash
export LABEL_STUDIO_API_KEY='paste-your-token-here'
python3 scripts/create_label_studio_projects.py --lead-gold
unset LABEL_STUDIO_API_KEY
```

This creates `CB-LEAD-GOLD-MASK`, `CB-LEAD-GOLD-PRESENCE`, and
`CB-LEAD-GOLD-QUALITY`, each with the correct 12 qualification images. Do not
invite coauthors into the lead instance or share these exports until all four
qualification submissions are locked.

### Manual project setup if the script cannot be used

For each applicable row in `label-studio/project_plan.csv`:

1. In Label Studio, choose **Create Project**.
2. Use the exact value in `project_name`.
3. Under **Labeling Setup**, choose **Code** and paste the entire XML file named
   in `label_config`.
4. Save the project.
5. Open **Import** and upload the JSON file named in `task_file`.
6. Confirm the displayed task count equals `image_count`.
7. Open the first task and confirm that the image loads.

Stop and notify the lead if the count is wrong or an image does not load.

## Qualification procedure

The lead labels all 12 images in the three automatically created gold projects
and exports:

- original Label Studio JSON for all three projects;
- **Brush labels to NumPy and PNG** for the mask project.

The four coauthors complete their own qualification projects independently.
They must not discuss specific images, view the lead labels, or view one
another's labels before submitting.

The lead compares each coauthor with lead gold:

- mean mask Dice must be at least `0.75`;
- presence kappa must be at least `0.60`;
- quality kappa must be at least `0.60`;
- there must be no systematic rule violation such as labeling dry tan grass as
  green vegetation or calling natural erosion lines roads.

If any gate fails, the lead reviews the relevant numbered rules with that
coauthor, resets the qualification projects, and asks for one clean repeat.
Never alter a submitted result to manufacture a pass.

Repeat the same 12-frame qualification check midway through production as the
manual requires. Pause a drifting annotator until they re-align.

## Calibration procedure

All four coauthors label the same 30 calibration images independently.

1. Everyone labels the first five images.
2. The lead exports those first-five results and holds a short alignment
   meeting.
3. Discuss rules and boundaries, not who was "right."
4. Every unresolved interpretation enters `metadata/decision_log.csv`.
5. The lead assigns the next numbered rule and records whether it must be
   applied retrospectively.
6. Everyone completes the remaining 25 images independently.
7. The lead computes and records Dice and kappa before production starts.

Do not replace source passes with consensus labels. Original annotator exports
remain immutable; adjudication creates separate final records.

## Per-image annotator procedure

Work on only one project in one browser tab. Never open the labeling stream in
two tabs.

For each image:

1. Confirm the key resembles `img_006806.jpg`.
2. Set the image to 100% or 1:1 zoom.
3. Scan from top-left to bottom-right.
4. Complete the requested task using only visible pixels.
5. Use `uncertain` when the manual does not determine the answer. Never guess.
6. Add the frame and question to the decision log queue for the lead.
7. Re-check every required field.
8. Click **Submit**, not Skip.

Do not use the GPS, phase, filename time, flight path, public maps, another
coauthor's labels, or outside knowledge of the Grand Canyon to decide a visible
label.

### Mask project

The target is resolvable living green vegetation, not every plant.

1. At 100% zoom, include green, olive-green, and dark-green living vegetation.
2. Exclude tan/dry grass, rock, sand, water/algae ambiguity, unconfirmed shadow,
   haze, cloud, snow, and man-made surfaces.
3. Exclude connected regions smaller than four pixels.
4. Use the greater-than-50%-of-a-boundary-pixel rule.
5. Keep only `green_visible_vegetation` brush regions in the final mask.
   `background` smart points are correction prompts, not target regions.
6. Mark `uncertain_region=present` if ambiguity remains.
7. Inspect the full mask once with the overlay visible and once with it hidden.

The XML supports ordinary brush/eraser work immediately. For interactive SAM,
the lead connects the official Segment Anything backend under **Settings >
Model**, enables **Interactive preannotations**, and annotators enable
**Auto-Annotation**. A SAM proposal is only a proposal: correct every overrun
and omission before submitting.

### Presence project

Choose `yes`, `no`, or `uncertain` for all six features.

- Water: `yes` needs a contiguous roughly 20-pixel region that visibly reads as
  water in a channel or basin.
- Road/trail: `yes` needs at least two engineered cues. One cue is
  `uncertain`; a natural wash with no engineered cue is `no`.
- Building/structure: regular man-made geometry.
- Dense forest: continuous canopy larger than roughly one 4x4 cell.
- Snow/ice: soft terrain-conforming white cover, not rock or cloud.
- Cultivated field: geometric agricultural parcels or a center-pivot circle.

Judge each feature independently. Never infer a road because a building exists
or water because vegetation exists.

### Quality project

Complete all six fields:

- cloud: `none` under 5%, `partial` from 5% through 33%, `heavy` above 33%;
- clarity: `clear`, `moderate`, or `heavy`;
- balloon: `none` or `partial` if any envelope pixel remains after cropping;
- sharpness: `sharp` or `blurred` for directional edge smear;
- exposure: `ok`, `over`, or `under` using the manual's 10% clipping rule;
- glare: `none` or `present`.

Heavy cloud, heavy clarity loss, or partial balloon makes the frame an exclusion
candidate, but the annotator still completes and submits all three tasks.

## End-of-stage export and handoff

For every project:

1. Verify the project dashboard shows 100% complete.
2. Open **Export**.
3. Export the original **JSON**.
4. For mask projects, also export **Brush labels to NumPy and PNG**.
5. Name the files exactly:

```text
A1_qualification_mask.json
A1_qualification_presence.json
A1_qualification_quality.json
A1_calibration_mask.json
A1_calibration_presence.json
A1_calibration_quality.json
A1_production_mask.json
A1_production_presence.json
A1_production_quality.json
```

Replace `A1` with the assigned id. Do not rename individual images or masks.
Send the exports privately to the lead; do not commit raw Label Studio exports
to the public repository.

The lead converts categorical exports after receipt:

```bash
python3 scripts/convert_label_studio_choices.py \
  A1_qualification_presence.json \
  A1_calibration_presence.json \
  A1_production_presence.json \
  --task presence \
  --annotator A1 \
  --output labels/annotator/A1_presence.jsonl
```

Use the same command with `--task quality` and the three quality exports.
Masks remain per-annotator PNGs named `img_SSSSSS__A1.png`; retain the original
JSON so the lead can verify the image-to-mask mapping.

## Lead's weekly and final checks

Each week:

1. Back up all exports.
2. Check completion counts against `workload_summary.csv`.
3. Confirm no image appears in an annotator's work twice.
4. Review uncertainties and append decisions; never edit an earlier decision
   row in place.
5. Compute shared-set Dice and kappa.
6. Adjudicate conflicts into new files; never overwrite either source pass.

Before the first frozen release, the lead still must:

- document the final image-data license designation;
- obtain and record the reference imagery license;
- assign and complete registration with independent checking;
- publish registration residuals and exclude unreliable frames from grounding;
- complete the full release audit in `docs/release-audit.md`;
- add the Hugging Face/Zenodo release and DOI;
- replace citation placeholders.

Those release tasks do not block visible-image annotation.

## Troubleshooting

- **Image does not load:** open its `image_url` from the assignment CSV directly
  in a browser. If that also fails, stop and notify the lead with the exact
  filename.
- **Wrong task count:** delete the newly created project and rerun the project
  creation command. Do not continue with a partial import.
- **Docker container name already exists:** use
  `docker start -a canyonbench-label-studio`; do not create a second store.
- **A rule is ambiguous:** choose `uncertain`, submit, and send the frame plus
  the question to the lead. Do not improvise a private rule.
- **SAM is unavailable:** presence and quality can continue. Mask work can use
  the brush/eraser manually, or pause until the lead connects SAM.

Official references:
[Label Studio installation](https://labelstud.io/guide/install.html),
[task import](https://labelstud.io/guide/tasks),
[annotation export](https://labelstud.io/guide/export), and
[Segment Anything integration](https://labelstud.io/guide/ml_tutorials/segment_anything_model).
