# CanyonBench annotator instructions

Welcome to the CanyonBench annotation team.

This guide is written for someone who has never used GitHub, Python, Docker, or
Label Studio. Follow it from top to bottom. Do not skip ahead. You are not
expected to write code or understand the software internally.

If something does not look exactly as described, stop and send the project lead
the error message or a screenshot. Do not guess how to fix a partial project.

> ## ⛔ Calibration is paused — checkpoint 5 was reviewed and the imagery changed
>
> **Read [CHECKPOINT5_REVIEW.md](CHECKPOINT5_REVIEW.md) before labelling
> anything else.** Sammy: also read [GOLD_SET_REVIEW.md](GOLD_SET_REVIEW.md).
>
> Two things changed:
>
> 1. **You now label colour-corrected images.** The camera recorded with a bad
>    white balance that turned the whole scene blue and made vegetation
>    impossible to judge. Every task file now points at `frames_corrected/`.
>    **You must delete and recreate your projects** so they load the new images.
> 2. **The vegetation rules are rewritten.** Rules A-13 to A-17 replace the
>    withdrawn A-11 and A-12. Part 6 below has been updated to match.
>
> Presence and quality guidance is unchanged. Do not label calibration image 6
> until the lead sends `CONTINUE`.

## Read this first: the exact team and current plan

These assignments are final. Never exchange ids or use somebody else's id in a
command, project name, export filename, or Google Drive folder.

| Person | Permanent id | Role | Assigned images per project | First project command |
|---|---|---|---:|---|
| Sammy | `GOLD` | Private gold/reference annotator | 12 private reference images | `--lead-gold` |
| Atharva | `A1` | Independent production annotator | 168 | `--annotator A1 --stage CALIBRATION` |
| Pranav G. | `A2` | Independent production annotator | 167 | `--annotator A2 --stage CALIBRATION` |
| Kunsh | `A3` | Independent production annotator | 167 | `--annotator A3 --stage CALIBRATION` |
| Prabhav | `A4` | Independent production annotator | 168 | `--annotator A4 --stage CALIBRATION` |

Zafir has already tested and approved A1-A4. **Qualification is waived for this
run. A1-A4 must not create `QUALIFICATION` projects.** The qualification task
files remain in the repository only for Sammy's private gold work and the fresh
midpoint check.

The A1-A4 workflow is:

1. **CALIBRATION CHECKPOINT** - the first 5 of 30 images in each task;
2. **CALIBRATION FINAL** - all 30 images in each task;
3. **PRODUCTION FIRST HALF** - 84 images in each task;
4. **MIDPOINT** - a fresh 12-image check in each task;
5. **PRODUCTION FINAL** - finish all 167 or 168 images in each task;
6. export and upload every required file.

Every stage has three separate projects:

1. vegetation mask;
2. feature presence;
3. image quality.

## Fixed deadline

The annotation sprint restarts from the checkpoint on colour-corrected images.
The **August 20, 2026** freeze is unchanged — the lost days come out of buffer.

| Date | Who | What must be done |
|---|---|---|
| **Jul 29** | Lead | Corrected frames published; reviews sent to everyone |
| **Jul 29** | Sammy | Redo all 12 gold frames on corrected images |
| **Jul 29** | A1–A4 | Recreate calibration projects; redo the 5-image mask checkpoint; upload |
| **Jul 30** | Everyone | Re-alignment meeting. Lead sends `CONTINUE` |
| **Jul 30–31** | A1–A4 | Finish the remaining 25 calibration masks; upload `calibration_final` |
| **Jul 31** | Lead | Score calibration agreement; send `START PRODUCTION` |
| **Aug 1–3** | A1–A4 | First 84 production tasks in each of the three projects |
| **Aug 3** | A1–A4 | Stop at 84; complete the midpoint check; upload |
| **Aug 4** | Lead + Sammy | Midpoint review; send `RESUME PRODUCTION` |
| **Aug 4–7** | A1–A4 | Finish production; upload `production_final` |
| **Aug 8–10** | Lead | Import validation, agreement, adjudication |
| **Aug 11–12** | Lead | Freeze labels, masks, grounding inputs |
| **Aug 13–17** | Lead | Benchmark evaluation |
| **Aug 18–19** | Lead | Analysis, tables, figures |
| **Aug 20** | Lead | Reproducibility run and release freeze |

Only the three authorisation messages move you between stages: `CONTINUE` after
the 5-image checkpoint, `START PRODUCTION` after calibration, and
`RESUME PRODUCTION` after the midpoint. If anything threatens a date, tell the
lead the same day, not at the end of the stage.

The reference-imagery dependency was resolved on July 26: the project uses
public-domain 2023 USGS NAIP, streamed through QGIS in `EPSG:26912`. A1–A4 do
not need QGIS or reference imagery.

## Shared Google Drive submission folder

Zafir will send one Google Drive link shared with the team. The link is a
submission location; it is not an invitation to review another person's work.

The Drive root must contain these folders:

```text
CanyonBench Annotation Submissions/
  A1_Atharva/
    calibration_checkpoint5/
    calibration_final/
    midpoint/
    production_final/
  A2_Pranav_G/
    calibration_checkpoint5/
    calibration_final/
    midpoint/
    production_final/
  A3_Kunsh/
    calibration_checkpoint5/
    calibration_final/
    midpoint/
    production_final/
  A4_Prabhav/
    calibration_checkpoint5/
    calibration_final/
    midpoint/
    production_final/
```

Each annotator uploads only to their own folder. Do not open, preview, download,
rename, move, or delete anything inside another annotator's folder. Because the
folder is shared by link, scientific independence depends on following this
rule exactly.

Sammy's gold exports must **not** go in this shared folder while A1-A4 are still
working. Sammy sends gold exports to Zafir through a separate private folder
accessible only to Sammy and Zafir. Zafir may move them into the project archive
after all production exports are locked.

Use this private gold folder structure:

```text
CanyonBench Gold Private/
  Sammy_gold_final/
```

Before starting, confirm that you have:

- your fixed id from the table above;
- the shared Google Drive link;
- edit access to your own named folder;
- confirmation from Zafir that the annotation sprint has started.

## What you need and do not need

You need:

- a Mac or Windows computer;
- a stable internet connection;
- approximately 3 GB of free disk space;
- permission to install Docker Desktop;
- Python 3.11 or newer;
- a modern browser such as Chrome, Edge, Firefox, or Safari;
- uninterrupted time to finish at least one image before pausing.

You do **not** need:

- the 71 GB Google Drive footage;
- the CanyonBench code repository;
- QGIS or registration imagery;
- a GPU;
- programming experience;
- a GitHub account if you use the ZIP download instructions;
- to make commits, branches, or pull requests.

The 377 selected images are already hosted publicly. Label Studio loads them
from the internet.

## Important independence rules

The scientific value of this dataset depends on independent annotations.

Do not:

- look at another annotator's labels, masks, exports, screen, or project;
- show another annotator your labels before the lead says comparison is allowed;
- open another annotator's files merely because the shared Drive link permits
  it;
- discuss what a particular image contains during calibration, midpoint, or
  production unless Zafir is leading an adjudication meeting;
- open maps, GPS coordinates, satellite imagery, or the raw flight path;
- use outside knowledge of the Grand Canyon to decide a label;
- ask an AI system to label an image;
- submit an uncorrected Segment Anything proposal;
- invent a new rule when uncertain;
- change an answer simply to agree with someone else.

You may ask the lead procedural questions such as "Where is the Export button?"
For a labeling ambiguity, submit `uncertain` where available and send the lead
the question template later in this guide.

## Part 1: install the required software

You need Docker Desktop and Python. You need to do this only once.

### Mac installation

#### Step 1A: install Docker Desktop

1. Open the official
   [Docker Desktop for Mac instructions](https://docs.docker.com/desktop/setup/install/mac-install/).
2. Choose the correct download:
   - **Apple silicon** for an M-series Mac such as M1, M2, M3, M4, or later;
   - **Intel** for an older Intel Mac.
3. Open the downloaded `Docker.dmg`.
4. Drag Docker into **Applications**.
5. Open **Applications > Docker**.
6. Accept Docker's terms if prompted.
7. Choose the recommended settings.
8. Wait until Docker reports that it is running. The first launch can take
   several minutes.

To verify it:

1. Press `Command + Space`.
2. Type `Terminal`.
3. Press Enter.
4. Copy and paste:

```bash
docker --version
```

5. Press Enter.

Success looks like a line beginning with `Docker version`. If you see
`command not found`, Docker is not fully installed or has not finished starting.

#### Step 1B: check or install Python

In the same Terminal window, paste:

```bash
python3 --version
```

Success looks like `Python 3.11`, `Python 3.12`, `Python 3.13`, or newer.

If the command is missing or the version is older than 3.11:

1. Visit [python.org/downloads](https://www.python.org/downloads/).
2. Download the current Python 3 installer for macOS.
3. Open the installer and use the default options.
4. Close Terminal completely and open it again.
5. Run `python3 --version` again.

You do not need to install any Python packages. The setup script uses only
Python's built-in features.

### Windows installation

Use **PowerShell**, not the older Command Prompt.

#### Step 1A: install Docker Desktop

1. Open the official
   [Docker Desktop for Windows instructions](https://docs.docker.com/desktop/setup/install/windows-install/).
2. Download Docker Desktop.
3. Open `Docker Desktop Installer.exe`.
4. Use the recommended per-user installation.
5. Keep **Use WSL 2 instead of Hyper-V** selected when offered.
6. Finish installation and restart the computer if requested.
7. Open Docker Desktop from the Start menu.
8. Wait until Docker reports that it is running.

To verify it:

1. Open the Start menu.
2. Type `PowerShell`.
3. Open **Windows PowerShell** or **Terminal** with a PowerShell tab.
4. Paste:

```powershell
docker --version
```

5. Press Enter.

Success begins with `Docker version`. If Docker mentions WSL or virtualization,
follow the link in the error message or send a screenshot to the lead. Do not
change BIOS settings unless you understand the change or have technical help.

#### Step 1B: check or install Python

In PowerShell, paste:

```powershell
py --version
```

Success looks like `Python 3.11`, `Python 3.12`, `Python 3.13`, or newer.

If `py` is not recognized:

1. Visit [python.org/downloads](https://www.python.org/downloads/).
2. Download the current Windows Python 3 installer.
3. Open the installer.
4. If the installer offers **Add Python to PATH**, select it.
5. Complete installation.
6. Close PowerShell completely and open it again.
7. Run `py --version` again.

## Part 2: download the annotation repository

The simplest method is a ZIP file. It does not require a GitHub account or Git.

### Recommended method: download a ZIP

1. Open
   [github.com/ZShamsi987/canyonbench-data](https://github.com/ZShamsi987/canyonbench-data).
2. Find the green **Code** button near the upper-right side of the file list.
3. Click **Code**.
4. Click **Download ZIP**.
5. Wait for the download to finish. It is roughly 50 MiB, not 71 GB.
6. Extract the ZIP:
   - Mac: double-click `canyonbench-data-main.zip`;
   - Windows: right-click the ZIP, choose **Extract All**, and then **Extract**.
7. The extracted folder should be named `canyonbench-data-main`.
8. Leave this folder in Downloads unless you intentionally move it.

Do not open or edit the 377 JPEGs outside Label Studio. The folder also contains
the setup script and these instructions.

### Optional method: GitHub Desktop

Use this only if you already prefer GitHub Desktop.

1. Install [GitHub Desktop](https://desktop.github.com/).
2. Open **File > Clone repository**.
3. Select the **URL** tab.
4. Enter:

```text
https://github.com/ZShamsi987/canyonbench-data.git
```

5. Choose a local folder.
6. Click **Clone**.

You do not need to make commits or push anything.

## Part 3: start your private Label Studio

Each annotator uses a separate Label Studio instance stored on their own
computer. This prevents accidental viewing or overwriting of another
annotator's work.

### Mac: start Label Studio for the first time

1. Make sure Docker Desktop is open and says it is running.
2. Open Terminal.
3. Paste this entire block:

```bash
mkdir -p "$HOME/canyonbench-label-studio"
docker run --name canyonbench-label-studio -it \
  -p 8080:8080 \
  -v "$HOME/canyonbench-label-studio:/label-studio/data" \
  heartexlabs/label-studio:latest
```

4. Press Enter.
5. Docker may download Label Studio. The first download can take several
   minutes and print many lines.
6. Leave this Terminal window open.
7. When the output stops changing rapidly, open:
   [http://localhost:8080](http://localhost:8080).

### Windows: start Label Studio for the first time

1. Make sure Docker Desktop is open and says it is running.
2. Open PowerShell.
3. Paste this entire block:

```powershell
$annotatorData = Join-Path $HOME "canyonbench-label-studio"
New-Item -ItemType Directory -Force $annotatorData
docker run --name canyonbench-label-studio -it `
  -p 8080:8080 `
  -v "${annotatorData}:/label-studio/data" `
  heartexlabs/label-studio:latest
```

4. Press Enter.
5. Docker may download Label Studio. The first download can take several
   minutes.
6. Leave PowerShell open.
7. Open [http://localhost:8080](http://localhost:8080).

`localhost` means this computer. Your projects are not publicly hosted.

### Create the local Label Studio account

The first time Label Studio opens:

1. Create an account using an email address and password you will remember.
2. This account belongs to your local Label Studio installation.
3. Do not share the password.
4. Do not invite another coauthor into this instance.

### Copy your API key

The setup script needs an API key so it can create the correct projects.

1. In Label Studio, open **Account & Settings**.
2. Open either **Personal Access Token** or **Legacy Token**:
   - if you use **Personal Access Token**, click **Create**, copy the token
     immediately, and save it temporarily because it is shown only once;
   - if you use **Legacy Token**, reveal and copy the existing token.
3. The CanyonBench setup script automatically accepts either type.
4. Keep it private. Do not paste it into chat or a shared document.
5. Return to Terminal or PowerShell.

## Part 4: create your calibration projects

Before running a command, replace `A1` with your assigned id. For example, an
annotator assigned `A3` must type `A3`.

Do not type `--stage QUALIFICATION`. Qualification has been waived for A1-A4.
Your first stage is `CALIBRATION`.

### Mac commands

If you downloaded the ZIP, paste:

```bash
cd "$HOME/Downloads/canyonbench-data-main"
```

If you moved the folder, type `cd ` with a space, drag the
`canyonbench-data-main` folder into Terminal, and press Enter.

Confirm you are in the correct folder:

```bash
pwd
test -f scripts/create_label_studio_projects.py && echo "Correct folder"
```

You must see `Correct folder`.

Now paste the following, replacing the token and `A1`:

```bash
export LABEL_STUDIO_API_KEY='paste-your-private-token-here'
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage CALIBRATION
unset LABEL_STUDIO_API_KEY
```

### Windows PowerShell commands

If you downloaded the ZIP, paste:

```powershell
Set-Location "$HOME\Downloads\canyonbench-data-main"
```

If you moved the folder:

1. Open the folder in File Explorer.
2. Click the address bar.
3. Copy the full folder path.
4. In PowerShell type `Set-Location ` followed by the quoted path.

Confirm you are in the correct folder:

```powershell
Get-Location
Test-Path "scripts\create_label_studio_projects.py"
```

The second command must print `True`.

Now paste the following, replacing the token and `A1`:

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-private-token-here"
py scripts/create_label_studio_projects.py --annotator A1 --stage CALIBRATION
Remove-Item Env:LABEL_STUDIO_API_KEY
```

### What success looks like

For annotator `A1`, the output should mention:

```text
CREATED CB-A1-CALI-MASK: 30 tasks
CREATED CB-A1-CALI-PRESENCE: 30 tasks
CREATED CB-A1-CALI-QUALITY: 30 tasks
Created 3 project(s) for A1 CALIBRATION.
```

Your id will appear instead of `A1`.

Open [http://localhost:8080/projects](http://localhost:8080/projects). Confirm
that you see exactly these three new projects:

```text
CB-A1-CALI-MASK
CB-A1-CALI-PRESENCE
CB-A1-CALI-QUALITY
```

Each project must contain exactly 30 images.

If the count is wrong, an image is broken, or only some projects were created,
stop and send the lead the complete Terminal/PowerShell output.

### What the project script imports

The script performs the import automatically. It combines one task list with
one labeling interface:

| Stage/project type | Task JSON imported | Labeling configuration | Expected tasks |
|---|---|---|---:|
| Calibration mask | `label-studio/tasks/shared_calibration_30.json` | `label-studio/vegetation-mask.xml` | 30 |
| Calibration presence | `label-studio/tasks/shared_calibration_30.json` | `label-studio/presence.xml` | 30 |
| Calibration quality | `label-studio/tasks/shared_calibration_30.json` | `label-studio/quality.xml` | 30 |
| Production, all three types | `label-studio/tasks/A1_production.json` using your own id | matching mask/presence/quality XML | 167 or 168 |
| Midpoint, all three types | `label-studio/tasks/qualification_12.json` | matching mask/presence/quality XML | 12 |
| Sammy gold, all three types | `label-studio/tasks/qualification_12.json` | matching mask/presence/quality XML | 12 |

These JSON files contain public image URLs. Do not import the `frames` folders,
individual JPEGs, a CSV, or the repository ZIP.

### Manual import fallback

Use this only if Zafir specifically tells you the automatic script cannot be
used. Never create a manual project in addition to a correct automatic project.

For each required project:

1. Open Label Studio's **Projects** page.
2. Click **Create Project**.
3. Enter the exact project title from this guide.
4. Open **Labeling Setup**.
5. Choose the **Code** or XML editor.
6. On the computer, open the matching XML file from `label-studio`.
7. Copy the entire file, including the opening and closing `<View>` lines.
8. Paste it into Label Studio's code editor, replacing any example content.
9. Save the labeling setup.
10. Open the project's **Import** screen.
11. Upload the one matching JSON task file from `label-studio/tasks`.
12. Complete the import.
13. Confirm the exact task count.
14. Open the first task and confirm the full image and correct controls load.
15. Repeat for the other two project types.

Stop if the count or interface differs. Do not try several imports into the same
project, because that can duplicate tasks.

## Sammy only: create the private gold/reference set

This section is only for Sammy. A1-A4 skip it.

Sammy is the separate gold/reference annotator, not A1, A2, A3, or A4. The gold
set is used for quality control and adjudication. Because Zafir waived the
qualification gate for the trusted production annotators, it does not delay
their start.

Sammy follows Parts 1-3 to install and start a separate private Label Studio
instance. From the downloaded repository folder, run:

Mac:

```bash
export LABEL_STUDIO_API_KEY='paste-your-private-token-here'
python3 scripts/create_label_studio_projects.py --lead-gold
unset LABEL_STUDIO_API_KEY
```

Windows PowerShell:

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-private-token-here"
py scripts/create_label_studio_projects.py --lead-gold
Remove-Item Env:LABEL_STUDIO_API_KEY
```

Success creates:

```text
CB-LEAD-GOLD-MASK
CB-LEAD-GOLD-PRESENCE
CB-LEAD-GOLD-QUALITY
```

Each project must contain exactly 12 images.

Sammy then:

1. completes all 12 mask tasks using Part 6;
2. completes all 12 presence tasks using Part 7;
3. completes all 12 quality tasks using Part 8;
4. verifies every project shows `12 of 12` complete;
5. follows Part 11 to export four files;
6. names them exactly:

```text
Sammy_gold_mask.json
Sammy_gold_mask_png.zip
Sammy_gold_presence.json
Sammy_gold_quality.json
```

7. uploads them to the separate Sammy-and-Zafir private Drive folder;
8. tells Zafir the upload is complete;
9. does not upload them into the shared A1-A4 folder or show them to A1-A4
   before their production exports are locked.

## Part 5: understand the annotation screen

Open only one project in one browser tab.

1. Click the project.
2. Click **Label All Tasks**.
3. Wait for the full image to load.
4. Do not work from the small Data Manager thumbnail.
5. Use the zoom control to inspect the image at 100% or 1:1.
6. Pan through the complete image from upper-left to lower-right.
7. Complete every required field.
8. Re-check the result.
9. Click **Submit**, not Skip.

Never open **Label All Tasks** in two tabs. Doing so can create duplicate or
conflicting work.

### Exact daily annotation loop

Use this loop every time you sit down to work:

1. Open Docker Desktop and wait until it says it is running.
2. Start or resume the `canyonbench-label-studio` container.
3. Open [http://localhost:8080](http://localhost:8080).
4. Open exactly one authorized project.
5. Confirm the project title contains your own id.
6. Confirm its total task count is correct before labeling.
7. Click **Label All Tasks**.
8. On each image, wait for the full-resolution image to finish loading.
9. Inspect at 100% zoom from upper-left to lower-right.
10. Complete every field or mask required by that project.
11. Review the result once before submitting.
12. Click **Submit**. Never click **Skip**.
13. Confirm the next image appears and the completed count increased.
14. Stop at the exact checkpoint count required by this guide.
15. Before ending the day, export any required checkpoint and upload a copy to
    your own Google Drive folder.

If you accidentally open the wrong person's project or the wrong stage, close
it without submitting anything and tell Zafir. If you accidentally submit a
mistake, record the filename and tell Zafir; do not conceal it or improvise a
repair.

Within a checkpoint, work on the project types in this order:

1. all images in the mask project;
2. all images in the presence project;
3. all images in the quality project.

For example, at the five-image calibration checkpoint, submit five mask tasks,
then five presence tasks, then five quality tasks. Do not finish all 30 mask
tasks before completing the required five-image checkpoint in the other two
projects.

## Part 6: how to label vegetation masks

Open the project ending in `-MASK`.

> **Before you start, open the vegetation reference card:**
> [figures/fig2_vegetation_reference.png](figures/fig2_vegetation_reference.png)
> Keep it visible in a second window. It shows real examples of what to mask and
> what not to mask, taken from these exact frames.

### The one test that decides everything

> **A region is vegetation only if GREEN is its strongest colour channel.**

Not "darker than its surroundings". Not "greyer". Not "different". **Green** —
the way a lawn or a tree is green.

On the corrected images, vegetation here is usually **dark green**, with a
typical colour around RGB (45–75, 70–100, 45–75). Bare desert is orange-brown
with red clearly strongest. If you are unsure about a patch, ask yourself: *if I
saw this on its own with no surroundings, would I call it green?* If the answer
is no, do not mask it.

### The four traps — none of these is vegetation

These caused every mask error at checkpoint 5. Learn them.

| Trap | Why it fools you | How to tell | Rule |
|---|---|---|---|
| **Darker brown rock** | Different rock units differ in brightness, so a patch looks "different" | Red still beats green. Brightness is not hue | A-15 |
| **Shadow** | Dark, and it was blue before correction | Branches and follows topography; no green hue | A-8 |
| **Water** | Can appear green, teal or turquoise | Sits in a basin with a level shoreline | A-8 |
| **Olive tint with no edge** | A faint wash across a whole slope at high altitude | You cannot draw a boundary around it | A-6 |

### Haze: it hides vegetation, it never creates it

The correction removed the camera's blue colour cast. It did **not** remove
haze, on purpose, because `clarity` still has to measure it.

So on a hazy frame: mask only what you can actually see. Do not infer vegetation
from a general olive cast and do not mask more generously to compensate. If the
haze is hiding things, that is what the `clarity` flag is for. (Rule A-16)

### How much vegetation to expect

Measured across all 377 frames after correction:

| Vegetation in a frame | How many frames |
|---|---|
| Under 0.1% | 295 of 377 |
| 0.1% – 0.5% | 60 of 377 |
| Over 0.5% | 22 of 377 |
| Over 1% | 7 of 377 |

**The most vegetated frame in the whole dataset is 2.4%. The median is 0.009%.**

If you are masking 10% or 20% of a frame, something has gone wrong — that is
hundreds of times more vegetation than exists anywhere in this dataset. A few
small patches, or none at all, is the normal correct answer. (Rule A-17)

### Include

Include a region only when it is visibly:

- green — green is the strongest channel, not merely a darker shade;
- living vegetation;
- resolved clearly enough that you could trace its boundary;
- at least four connected pixels.

Typical real examples in this dataset: a dark green ribbon along a wash, street
trees and watered yards near Page, an irrigated field.

### Exclude

Do not mask:

- darker or greyer rock that is not actually green;
- shadow, including shadow that looked blue before correction;
- water, whatever colour it appears — including turquoise ponds;
- a faint olive wash you cannot resolve into distinct patches;
- tan, straw-coloured, dry or brown grass;
- bare rock, red rock, sand, or mineral tint;
- cloud, haze, snow, ice, glare, or balloon material;
- roads, roofs, vehicles, or other man-made surfaces;
- isolated one-to-three-pixel green noise.

### Paint the mask

1. Find the brush-label controls beside or below the image.
2. Select the brush label named `green_visible_vegetation`.
3. Zoom to 100% and work through the frame left-to-right, top-to-bottom.
4. Press and hold the primary mouse/trackpad button while moving to paint.
5. Use a small brush so narrow vegetation is not covered by an oversized stroke.
6. Select the eraser and remove every spill onto rock, water, or shadow.
7. At a boundary, include a pixel only when vegetation occupies more than half
   of it.
8. Do not enlarge the mask "to be safe". An under-sized accurate mask is worth
   more than a generous one.
9. Inspect the whole image once with the overlay visible and once hidden.
10. Choose an uncertain-region answer.
11. Click **Submit** only when both the mask and the uncertainty choice are
    final.

If there is no qualifying green vegetation, leave the mask empty, choose
`uncertain_region=none`, and submit. **An empty mask is a complete, valid
answer** and on this dataset it is often the correct one.

### About the red `background` option

Do not paint the whole image red. `background` under the smart point controls is
only a negative correction prompt for an interactive Segment Anything setup. The
final mask must contain only `green_visible_vegetation`.

### If Segment Anything is available

- The proposal is not an answer.
- Zoom in and correct every overrun and omission.
- Delete incorrect proposals.
- Submit only after the result follows the human rules above.

### Uncertain-region field

Always choose one:

- `none` when no unresolved green-region ambiguity remains;
- `present` when a region could not be determined under the rules.

If you choose `present`, send the lead the image/question template after
submitting.

## Part 7: how to label feature presence

Open the project ending in `-PRESENCE`.

For every feature, choose:

- `yes` when the visible evidence meets the minimum;
- `no` when the feature is absent and there is no meaningful evidence;
- `uncertain` when there is some evidence but it is below the minimum or
  ambiguous.

Do not leave any feature unanswered.

For each image, click exactly one answer for each row in this order:

1. `water`;
2. `road`;
3. `building`;
4. `forest`;
5. `snow`;
6. `field`.

Before clicking **Submit**, count six selected answers. A selection in one row
does not answer any other row.

### Water

Choose `yes` only when:

- a contiguous region of roughly 20 pixels or more visibly reads as water;
- it has smooth texture, water color, or specular sheen;
- it lies in a plausible channel or basin rather than a shaded slope.

A tiny blue mark or ambiguous dark canyon shadow is `uncertain` or `no`, not an
automatic `yes`.

### Road or trail

Choose `yes` only when at least two engineered cues are visible:

- consistent width along its length;
- straight, hard, or smoothly engineered edges;
- a cut or embankment across terrain;
- a visible junction or vehicle;
- a connection to a structure.

Exactly one engineered cue means `uncertain`. A dry wash, natural erosion line,
or ridgeline with no engineered cues is `no`.

### Building or structure

Choose `yes` for regular man-made geometry such as:

- straight edges or right angles;
- a roof;
- a dam;
- a tower;
- another clearly constructed object.

Do not infer a building from a road alone.

### Dense forest

Choose `yes` only for continuous tree canopy covering an area larger than
roughly one cell of an imagined 4x4 image grid. Scattered shrubs are not dense
forest.

### Snow or ice

Choose `yes` only for soft, terrain-conforming white cover. Hard-edged bright
rock or wispy cloud is not snow.

### Cultivated field

Choose `yes` only for visible agricultural geometry such as:

- regular parcel boundaries;
- repeated field patterns;
- a center-pivot circle.

Do not infer cultivation merely because an area looks flat.

### Independence between features

Judge every feature from its own evidence:

- a building does not prove a road;
- vegetation does not prove water;
- water does not prove cultivated fields.

## Part 8: how to label image quality

Open the project ending in `-QUALITY`.

Complete all six fields.

For each image, click exactly one answer for each row in this order:

1. `cloud`;
2. `clarity`;
3. `balloon`;
4. `sharpness`;
5. `exposure`;
6. `glare`.

Before clicking **Submit**, count six selected answers.

### Cloud

- `none`: cloud or haze covers less than 5% of visible ground;
- `partial`: 5% through 33%;
- `heavy`: more than 33%.

### Clarity

- `clear`: texture and shadows are crisp;
- `moderate`: contrast is reduced, but features remain identifiable;
- `heavy`: ground is washed out and colors/details are strongly muted.

### Balloon

- `none`: no balloon-envelope pixel remains after the left crop;
- `partial`: any balloon envelope remains visible.

### Sharpness

- `sharp`: edges look crisp at 100%;
- `blurred`: edges have directional smear from motion or focus.

### Exposure

- `ok`: neither bright nor dark clipping dominates;
- `over`: clipped white highlights cover more than roughly 10%;
- `under`: crushed, detail-losing shadows cover more than roughly 10%.

### Glare

- `none`: no bright bloom or veiling flare;
- `present`: visible bright bloom, reflection, or flare obscures the scene.

Even if an image has heavy cloud, heavy clarity loss, or visible balloon, finish
all fields and submit it. The lead decides exclusions later.

## Part 9: what to do when uncertain

Do not guess and do not privately invent a new rule.

When a categorical task offers `uncertain`, choose it. For a mask ambiguity,
choose `uncertain_region=present`.

After submitting, send the lead:

```text
Annotator id:
Stage: calibration / midpoint / production
Project: mask / presence / quality
Image filename: img_XXXXXX.jpg
Question:
Rule(s) I checked:
What I submitted:
Screenshot, if useful:
```

You can find the image filename in the task metadata or Data Manager. The lead
will place the final decision in the shared decision log.

Do not silently return to old submissions and change them after learning
something new. The lead will tell everyone when a new rule must be applied
retrospectively.

## Part 10: pausing and resuming safely

### Pause annotation work

1. Finish the current image.
2. Click **Submit and Exit** if available, or submit and return to the project.
3. Confirm the project completion count increased.
4. Close the browser tab.
5. In the Terminal/PowerShell window running Docker, press `Control + C`.
6. Wait for the container to stop.

Your work remains in the `canyonbench-label-studio` data folder. Do not delete
that folder or the Docker container.

### Resume on another day

1. Open Docker Desktop and wait until it is running.
2. Open Terminal or PowerShell.
3. Run:

```text
docker start -a canyonbench-label-studio
```

4. Leave the window open.
5. Open [http://localhost:8080](http://localhost:8080).
6. Sign in and continue the incomplete project.

If Docker says the container name already exists, that is normally good: use
the resume command above. Do not delete and recreate the container, because the
existing container holds your project database.

## Part 11: exact export and Google Drive upload procedure

Every checkpoint or completed stage produces exactly four files:

1. mask project original JSON;
2. mask project PNG/NumPy archive;
3. presence project original JSON;
4. quality project original JSON.

Never upload your API token, the Label Studio data folder, screenshots containing
the token, or the repository ZIP.

### Export original JSON

Repeat these steps for the mask, presence, and quality projects:

1. Open the correct project.
2. Verify its completed count matches the checkpoint or final count.
3. Click **Export** in the project interface.
4. Choose the format named **JSON**, meaning original Label Studio JSON.
5. Do not choose `JSON_MIN`, CSV, COCO, or another converted format.
6. Click **Export** or **Download** and wait for the browser download to finish.
7. Find the downloaded file in the computer's **Downloads** folder.
8. Rename it to the exact stage filename shown later in this guide.

### Export the mask PNG/NumPy archive

For the mask project only:

1. Return to the mask project's **Export** screen.
2. Choose **Brush labels to NumPy and PNG**.
3. Start the export.
4. Wait until the ZIP/archive download is complete.
5. Do not unzip it, reorganize it, or rename files inside it.
6. Rename the complete archive to the exact `_mask_png.zip` filename shown in
   this guide.

If the browser downloaded an archive with another extension, keep the actual
extension and tell Zafir. Do not merely change a non-ZIP file's extension to
`.zip`.

### Rename files safely

- Mac: select the file in Finder, press Enter, type the exact name, and press
  Enter again.
- Windows: select the file in File Explorer, press `F2`, type the exact name,
  and press Enter.
- Do not add a second extension such as `.json.json` or `.zip.zip`.
- Every filename must begin with your exact id, not your name.

### Check the four files before upload

1. Confirm all four files exist.
2. Confirm none has a size of `0 bytes`.
3. Open each JSON file in a text editor and confirm it begins with `[` or `{`
   and contains text. Do not edit or re-save it.
4. Confirm the mask archive opens as a ZIP without an error, but do not modify
   its contents.
5. Keep an untouched local backup.

### Upload to the shared Google Drive

1. Open the Google Drive link sent by Zafir.
2. Open only your assigned root folder, such as `A1_Atharva`.
3. Open the correct stage subfolder.
4. Click **New > File upload**, or drag the four files into that subfolder.
5. Wait until Google Drive reports that every upload is complete.
6. Refresh the folder once.
7. Confirm that exactly four correctly named files are visible and each has a
   nonzero size.
8. Do not open or change another annotator's folder.
9. Send Zafir a short message in this format:

```text
UPLOAD COMPLETE
Annotator: A1 - Atharva
Stage: calibration checkpoint 5 / calibration final / midpoint / production final
Drive folder:
Mask JSON:
Mask PNG ZIP:
Presence JSON:
Quality JSON:
Completed count in each Label Studio project:
Problems or uncertainties:
```

Replace the example identity and stage with your own.

## Part 12: calibration

Part 4 already created these projects. Do not run the creation command again.

### Required five-image checkpoint

Do not complete all 30 immediately. Every annotator must:

1. label only the first five images in the mask project;
2. label only the first five images in the presence project;
3. label only the first five images in the quality project;
4. stop with exactly `5 of 30` completed in each project;
5. export the three current JSON files and the current mask PNG/NumPy archive;
6. name those checkpoint files:

```text
A1_calibration_checkpoint5_mask.json
A1_calibration_checkpoint5_mask_png.zip
A1_calibration_checkpoint5_presence.json
A1_calibration_checkpoint5_quality.json
```

7. upload the four files to your own `calibration_checkpoint5` Drive folder;
8. leave the local projects unchanged;
9. send Zafir the `UPLOAD COMPLETE` message;
10. attend the short alignment meeting and wait for the exact word
    **CONTINUE** before labeling image 6.

During the meeting, discuss the written rules and boundaries under the lead's
direction. Do not independently exchange or compare actual submissions with
coauthors.

After the lead says to continue:

1. return to the same three calibration projects;
2. complete the remaining 25 images in each;
3. verify each project now shows `30 of 30` complete;
4. export the final calibration files below.

Export and name the four calibration files:

```text
A1_calibration_mask.json
A1_calibration_mask_png.zip
A1_calibration_presence.json
A1_calibration_quality.json
```

Upload these four files to your own `calibration_final` Drive folder. Confirm
the folder contains exactly four nonempty files, send Zafir the completion
message, and wait for the exact words **START PRODUCTION**.

## Part 13: production

After the lead explicitly authorizes production, create the projects.

### Mac

```bash
export LABEL_STUDIO_API_KEY='paste-your-private-token-here'
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage PRODUCTION
unset LABEL_STUDIO_API_KEY
```

### Windows PowerShell

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-private-token-here"
py scripts/create_label_studio_projects.py --annotator A1 --stage PRODUCTION
Remove-Item Env:LABEL_STUDIO_API_KEY
```

Replace `A1` with your own id. Open the projects page and verify the exact titles
and counts:

| Person | ID | Expected project titles | Images in each project |
|---|---|---|---:|
| Atharva | A1 | `CB-A1-PROD-MASK`, `CB-A1-PROD-PRESENCE`, `CB-A1-PROD-QUALITY` | 168 |
| Pranav G. | A2 | `CB-A2-PROD-MASK`, `CB-A2-PROD-PRESENCE`, `CB-A2-PROD-QUALITY` | 167 |
| Kunsh | A3 | `CB-A3-PROD-MASK`, `CB-A3-PROD-PRESENCE`, `CB-A3-PROD-QUALITY` | 167 |
| Prabhav | A4 | `CB-A4-PROD-MASK`, `CB-A4-PROD-PRESENCE`, `CB-A4-PROD-QUALITY` | 168 |

If your count differs, stop before labeling.

Production uses the same mask, presence, and quality rules. Work carefully; do
not rush because the project is larger.

### Stop automatically at the production halfway point

Every annotator stops after exactly 84 completed tasks in **each** production
project:

1. complete mask tasks until the mask project shows `84` completed, then stop
   that project;
2. complete presence tasks until the presence project shows `84` completed,
   then stop that project;
3. complete quality tasks until the quality project shows `84` completed, then
   stop that project;
4. do not label task 85 in any production project yet.

Then:

1. record or screenshot the `84` completion count for all three production
   projects;
2. create three fresh midpoint projects using the commands below.

Mac:

```bash
export LABEL_STUDIO_API_KEY='paste-your-private-token-here'
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage MIDPOINT
unset LABEL_STUDIO_API_KEY
```

Windows PowerShell:

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-private-token-here"
py scripts/create_label_studio_projects.py --annotator A1 --stage MIDPOINT
Remove-Item Env:LABEL_STUDIO_API_KEY
```

Replace `A1` with your id. Success creates:

```text
CB-A1-MID-MASK
CB-A1-MID-PRESENCE
CB-A1-MID-QUALITY
```

Each midpoint project contains exactly 12 images.

1. Complete all 12 tasks in each midpoint project without opening any old
   `QUAL` project.
2. Verify every midpoint project shows `12 of 12` complete.
3. Export and name:

```text
A1_midpoint_mask.json
A1_midpoint_mask_png.zip
A1_midpoint_presence.json
A1_midpoint_quality.json
```

4. Upload the four files to your own `midpoint` Google Drive folder.
5. Send Zafir the `UPLOAD COMPLETE` message.
6. Wait for the exact words **RESUME PRODUCTION**.
7. Return to the same production projects.
8. Confirm each still shows exactly `84` completed.
9. Start at task 85 and finish every remaining task in this order: mask,
   presence, then quality.

At the end, confirm all three production projects show the final count from the
team table, then export:

```text
A1_production_mask.json
A1_production_mask_png.zip
A1_production_presence.json
A1_production_quality.json
```

Upload those four files to your own `production_final` Google Drive folder.
Refresh Drive, verify the names and nonzero sizes, keep your local backup, and
send the final `UPLOAD COMPLETE` message.

## Part 14: final completion checklist

Before telling the lead you are finished, confirm:

- [ ] I used only my assigned A1-A4 id.
- [ ] I did not create or label a `QUALIFICATION` project.
- [ ] I completed only authorized stages.
- [ ] Calibration, midpoint, and production projects show 100% complete.
- [ ] I never used Skip for a required image.
- [ ] I inspected masks at 100% zoom.
- [ ] I corrected automatic mask proposals.
- [ ] I answered every presence field.
- [ ] I answered every quality field.
- [ ] I used `uncertain` instead of guessing.
- [ ] I sent ambiguity questions to the lead.
- [ ] I did not view another annotator's labels.
- [ ] I kept original JSON exports.
- [ ] I kept mask PNG/NumPy export archives.
- [ ] Every export filename begins with my annotator id.
- [ ] I made a private backup.
- [ ] I uploaded only to my own named Google Drive folder.
- [ ] I did not open, move, rename, or delete another annotator's exports.

## Troubleshooting

### `docker: command not found` or `docker is not recognized`

Docker Desktop is not installed, not fully started, or Terminal/PowerShell was
opened before installation completed.

1. Open Docker Desktop.
2. Wait until it says it is running.
3. Close and reopen Terminal/PowerShell.
4. Run `docker --version`.

### `Cannot connect to the Docker daemon`

Docker Desktop is installed but not running. Open it and wait.

### `The container name ... is already in use`

Do not run the first-time `docker run` command again. Resume the saved instance:

```text
docker start -a canyonbench-label-studio
```

### Port 8080 is already allocated

Stop and ask the lead for help, or use port 8081.

In the Docker command, change:

```text
-p 8080:8080
```

to:

```text
-p 8081:8080
```

Open `http://localhost:8081` and add this to every project-creation command:

```text
--url http://localhost:8081
```

### Python command not found

- Mac: install Python, reopen Terminal, and run `python3 --version`.
- Windows: install Python, reopen PowerShell, and run `py --version`.

### `No such file or directory` or `can't open file`

You are not inside the extracted repository folder.

- Mac: run `cd "$HOME/Downloads/canyonbench-data-main"`.
- Windows: run
  `Set-Location "$HOME\Downloads\canyonbench-data-main"`.

Then verify the setup script exists as shown earlier.

### `Set LABEL_STUDIO_API_KEY`

The token was not copied into the environment, or the command window was
reopened. Repeat the token command and immediately rerun the setup command.

### HTTP 401 or 403

The API token is incorrect, expired, or was copied incompletely. The setup
script accepts both current personal access tokens and legacy tokens.

1. Return to Label Studio **Account & Settings**.
2. Create and copy a new personal access token, or copy the complete legacy
   token;
3. set it again;
4. rerun the command.

Do not send the token to the lead.

### Script says `SKIP existing project`

The project name already exists. Open Label Studio and inspect it.

- If it contains the correct task count and no incorrect annotations, continue.
- If it is partial or wrong, stop and ask the lead before deleting anything.

### An image does not load

1. Confirm the computer has internet access.
2. Wait 30 seconds and reload once.
3. Open the Data Manager and note the exact `img_XXXXXX.jpg` filename.
4. Stop if it still fails.
5. Send the filename and screenshot to the lead.

Do not substitute a different image.

### Browser is slow during masks

1. Close unrelated browser tabs and applications.
2. Work in only one Label Studio tab.
3. Finish and submit the current image before refreshing.
4. Restart the browser if necessary.
5. Never delete completed tasks to improve speed.

### You submitted a genuine mistake

Do not hide it.

1. Record the image filename.
2. Tell the lead what happened.
3. Change the annotation only if the lead instructs you to do so.

### Computer failure or lost local projects

Stop and tell the lead. Provide:

- your annotator id;
- completed stage and approximate count;
- the last exports you backed up;
- the error or failure description.

Do not recreate projects and begin from memory without coordinating with the
lead.

## Glossary

- **Annotation:** a human label saved for one image.
- **API key/token:** a private code that lets the setup script talk to your
  local Label Studio.
- **Calibration:** a shared set labeled independently by all four annotators so
  agreement can be measured.
- **Docker Desktop:** the application that runs Label Studio locally.
- **Export:** the saved JSON or mask archive returned to the lead.
- **GitHub:** the website hosting the public images and setup files.
- **Label Studio:** the browser application used to create annotations.
- **Mask:** a pixel-level painted region showing visible green vegetation.
- **Production:** your main assigned image set after calibration.
- **Qualification:** a standard 12-image gate that Zafir explicitly waived for
  A1-A4 in this run.
- **Gold/reference set:** Sammy's private 12-image reference annotations used
  for quality control and adjudication.
- **Repository:** the project folder downloaded from GitHub.
- **SAM / Segment Anything:** an optional tool that proposes a mask; a human
  must correct it.
- **Terminal / PowerShell:** the text window used to run copy-paste commands.
- **Uncertain:** the correct label when visible evidence does not meet a
  definitive rule.

## Authoritative references

For difficult labeling decisions, the
[numbered annotation manual](../docs/annotation-manual.md) is authoritative.
The [project lead guide](../docs/START_ANNOTATING.md) explains the current
qualification waiver, agreement, adjudication, registration, and release
duties.

Official software help:

- [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Label Studio installation](https://labelstud.io/guide/install.html)
- [Label Studio access tokens](https://labelstud.io/guide/access_tokens)
- [Label Studio labeling](https://labelstud.io/guide/labeling.html)
- [Label Studio export](https://labelstud.io/guide/export)

When software instructions conflict with an actual labeling rule, follow the
CanyonBench annotation manual and ask the lead.
