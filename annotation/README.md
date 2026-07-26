# CanyonBench annotator instructions

Welcome to the CanyonBench annotation team.

This guide is written for someone who has never used GitHub, Python, Docker, or
Label Studio. Follow it from top to bottom. Do not skip ahead. You are not
expected to write code or understand the software internally.

If something does not look exactly as described, stop and send the project lead
the error message or a screenshot. Do not guess how to fix a partial project.

## The one rule to remember

You will work in three stages:

1. **QUALIFICATION** - 12 images per task.
2. **CALIBRATION** - 30 images per task, only after the lead says you passed.
3. **PRODUCTION** - 167 or 168 images per task, only after the lead approves
   calibration.

Halfway through production, the lead will pause you for one fresh 12-image
**MIDPOINT** repeat. The software creates new projects for it, so you never
reopen or copy your original qualification answers.

For every stage, there are three separate projects:

1. vegetation mask;
2. feature presence;
3. image quality.

Create only the stage the lead has authorized. When you first receive this
guide, that stage is **QUALIFICATION**.

## What the project lead must send you

Before doing anything, you must receive:

- one permanent annotator id: `A1`, `A2`, `A3`, or `A4`;
- confirmation that you may start **QUALIFICATION**;
- the lead's preferred private method for returning exports, such as a private
  Drive folder or direct message.

Write your assigned id here before continuing:

```text
My permanent annotator id: A__
```

Use that same id everywhere. Do not use your name, initials, or another
coauthor's id in filenames or commands.

If the lead has not assigned an id, stop here and ask for one.

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
- discuss what a particular image contains during qualification or independent
  calibration;
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

## Part 4: create your qualification projects

Before running a command, replace `A1` with your assigned id. For example, an
annotator assigned `A3` must type `A3`.

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
  --stage QUALIFICATION
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
py scripts/create_label_studio_projects.py --annotator A1 --stage QUALIFICATION
Remove-Item Env:LABEL_STUDIO_API_KEY
```

### What success looks like

For annotator `A1`, the output should mention:

```text
CREATED CB-A1-QUAL-MASK: 12 tasks
CREATED CB-A1-QUAL-PRESENCE: 12 tasks
CREATED CB-A1-QUAL-QUALITY: 12 tasks
Created 3 project(s) for A1 QUALIFICATION.
```

Your id will appear instead of `A1`.

Open [http://localhost:8080/projects](http://localhost:8080/projects). Confirm
that you see exactly these three new projects:

```text
CB-A1-QUAL-MASK
CB-A1-QUAL-PRESENCE
CB-A1-QUAL-QUALITY
```

Each project must contain exactly 12 images.

If the count is wrong, an image is broken, or only some projects were created,
stop and send the lead the complete Terminal/PowerShell output.

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

Complete the three project types in this order:

1. all images in the mask project;
2. all images in the presence project;
3. all images in the quality project.

## Part 6: how to label vegetation masks

Open the project ending in `-MASK`.

The target is **visible living green vegetation**. The target is not every plant
and not every naturally colored area.

### Include

Include a region only when it is visibly:

- green, olive-green, or dark-green;
- living vegetation;
- resolved clearly enough to trace;
- at least four connected pixels.

Examples include a resolvable green riverbank ribbon, tree canopy, shrubs, or a
green field.

### Exclude

Do not mask:

- tan, straw-colored, dry, or brown grass;
- bare rock, red rock, sand, or mineral tint;
- water or an uncertain algae/water region;
- cloud, haze, snow, ice, glare, or balloon material;
- shadow unless the vegetation remains clearly identifiable;
- roads, roofs, vehicles, or other man-made surfaces;
- a vague green wash that cannot be resolved into patches;
- isolated one-to-three-pixel green noise.

### Paint the mask

1. Select `green_visible_vegetation`.
2. Use the brush to paint only target vegetation.
3. Adjust brush size for the object.
4. Use the eraser to correct every spill outside vegetation.
5. At a boundary, include a pixel only when vegetation occupies more than half
   of that pixel.
6. Do not make the mask larger merely to be safe.
7. Inspect the entire image a second time before submitting.

If there is no qualifying green vegetation, leave the green mask empty.

### About the red `background` option

Do not paint the whole image red. `background` is only a negative correction
prompt for an interactive Segment Anything setup. The final target mask must
contain only `green_visible_vegetation`.

### If Segment Anything is available

Segment Anything may propose a mask after foreground/background clicks.

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
Stage: qualification / calibration / production
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

## Part 11: export qualification results

Export only after each project shows 100% complete.

Create a private folder on your computer:

```text
CanyonBench exports/
  A1/
    qualification/
```

Replace `A1` with your id.

### Export the mask project

1. Open the completed `CB-A1-QUAL-MASK` project.
2. Open **Export**.
3. Export the original Label Studio **JSON**.
4. Rename it:

```text
A1_qualification_mask.json
```

5. Export **Brush labels to NumPy and PNG**.
6. Keep the complete downloaded ZIP/archive together.
7. Rename the archive:

```text
A1_qualification_mask_png.zip
```

### Export the presence project

1. Open `CB-A1-QUAL-PRESENCE`.
2. Export the original **JSON**.
3. Rename it:

```text
A1_qualification_presence.json
```

### Export the quality project

1. Open `CB-A1-QUAL-QUALITY`.
2. Export the original **JSON**.
3. Rename it:

```text
A1_qualification_quality.json
```

### Qualification handoff checklist

You should send the lead exactly four files:

```text
A1_qualification_mask.json
A1_qualification_mask_png.zip
A1_qualification_presence.json
A1_qualification_quality.json
```

Before sending:

- replace `A1` with your id;
- open each JSON file and confirm it is not empty;
- confirm the ZIP/archive is not empty;
- keep your own untouched backup;
- send through the lead's private channel;
- do not upload exports to the public GitHub repository;
- do not send them to other annotators.

Wait for the lead to say either:

- **qualification passed; start calibration**, or
- **review required; do not continue yet**.

Do not create calibration projects until you receive the first message.

## Part 12: calibration

After the lead explicitly authorizes calibration, create the projects.

### Mac

From the repository folder:

```bash
export LABEL_STUDIO_API_KEY='paste-your-private-token-here'
python3 scripts/create_label_studio_projects.py \
  --annotator A1 \
  --stage CALIBRATION
unset LABEL_STUDIO_API_KEY
```

### Windows PowerShell

```powershell
$env:LABEL_STUDIO_API_KEY = "paste-your-private-token-here"
py scripts/create_label_studio_projects.py --annotator A1 --stage CALIBRATION
Remove-Item Env:LABEL_STUDIO_API_KEY
```

Replace `A1` with your id.

Success creates:

```text
CB-A1-CALI-MASK
CB-A1-CALI-PRESENCE
CB-A1-CALI-QUALITY
```

Each contains 30 images.

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

7. send the four files privately to the lead;
8. leave the local projects unchanged;
9. wait for the lead's alignment meeting and explicit permission to continue.

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

Wait for explicit production authorization.

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

Expected image counts:

| Annotator id | Images in each production project |
|---|---:|
| A1 | 168 |
| A2 | 167 |
| A3 | 167 |
| A4 | 168 |

If your count differs, stop before labeling.

Production uses the same mask, presence, and quality rules. Work carefully; do
not rush because the project is larger.

The lead will schedule a midpoint qualification repeat. When instructed:

1. pause production;
2. finish and submit the production image currently open;
3. record the completion count of each production project;
4. create three fresh midpoint projects using the commands below.

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

1. Complete those three projects without reopening the old `QUAL` projects.
2. Export and privately send:

```text
A1_midpoint_mask.json
A1_midpoint_mask_png.zip
A1_midpoint_presence.json
A1_midpoint_quality.json
```

3. Wait for the lead to confirm that you may resume production.
4. Return to the same production projects and confirm their completion counts
   match the counts you recorded before the midpoint repeat.

At the end, export:

```text
A1_production_mask.json
A1_production_mask_png.zip
A1_production_presence.json
A1_production_quality.json
```

## Part 14: final completion checklist

Before telling the lead you are finished, confirm:

- [ ] I used only my assigned A1-A4 id.
- [ ] I completed only authorized stages.
- [ ] Every project shows 100% complete.
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
- [ ] I sent exports only to the lead.

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
- **Production:** your main assigned image set after qualification/calibration.
- **Qualification:** the first 12-image gate checked against private lead gold.
- **Repository:** the project folder downloaded from GitHub.
- **SAM / Segment Anything:** an optional tool that proposes a mask; a human
  must correct it.
- **Terminal / PowerShell:** the text window used to run copy-paste commands.
- **Uncertain:** the correct label when visible evidence does not meet a
  definitive rule.

## Authoritative references

For difficult labeling decisions, the
[numbered annotation manual](../docs/annotation-manual.md) is authoritative.
The [project lead guide](../docs/START_ANNOTATING.md) explains qualification,
agreement, adjudication, registration, and release duties.

Official software help:

- [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Label Studio installation](https://labelstud.io/guide/install.html)
- [Label Studio access tokens](https://labelstud.io/guide/access_tokens)
- [Label Studio labeling](https://labelstud.io/guide/labeling.html)
- [Label Studio export](https://labelstud.io/guide/export)

When software instructions conflict with an actual labeling rule, follow the
CanyonBench annotation manual and ask the lead.
