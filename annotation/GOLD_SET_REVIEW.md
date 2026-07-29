# Gold Set Review — Sammy

**Revision 2, supersedes everything published before it.** Revision 1 said the
correct mask on all 12 gold frames was empty. That was wrong and has been
replaced. Section 2 of revision 1 — the `uncertain` finding — was correct and is
repeated here, because it is still the most important issue.

> ### ⚠️ Note on the midpoint check
>
> This page contains the reference answers for the 12 qualification images, and
> the same 12 are reused for the mid-production drift check. The lead has chosen
> to keep the same 12 rather than re-draw them. **A1–A4: do not read Section 3
> of this page before completing your midpoint projects.** For the paper, the
> midpoint is a consistency check, not a blind drift measurement.

---

## 0. What changed

| | Revision 1 (wrong) | Revision 2 (this page) |
|---|---|---|
| Which images you label | `frames/` | **`frames_corrected/`** |
| Correct mask on the 12 gold frames | "empty on all 12" | **small but real on most** |
| The three frames you left empty | "the three you got right" | only one is genuinely near-empty |
| The `uncertain` finding | — | **unchanged, still the main issue** |
| Exposure finding | — | **unchanged** |

Revision 1 measured greenness on the raw frames, which still carried the
camera's blue/violet colour cast. That was the wrong test. Corrected, these
frames do contain vegetation.

Your masks were still far too large — but the reason was that the imagery made
the question unanswerable, not that you were careless.

---

## 1. Masks — the real numbers

Read [CHECKPOINT5_REVIEW.md](CHECKPOINT5_REVIEW.md) Part 2 first. It has the
vegetation reference card, which is the thing to work from.

Measured on the corrected frames:

| Frame | You masked | Actually vegetation | Largest real patch |
|---|---:|---:|---:|
| `img_003522` | 32.1% | 0.075% | 110 px |
| `img_004422` | 45.5% | 0.248% | 70 px |
| `img_005564` | 15.9% | 0.091% | 44 px |
| `img_006404` | 20.0% | 0.096% | 72 px |
| `img_009710` | *empty* | 0.001% | 9 px |
| `img_010196` | *empty* | 0.000% | 0 px |
| `img_011104` | *empty* | 0.002% | 9 px |
| `img_015013` | 18.7% | 0.004% | 5 px |
| `img_018287` | 3.9% | 0.000% | 0 px |
| `img_021152` | 3.0% | 0.001% | 6 px |
| `img_022256` | 52.1% | 0.013% | 19 px |
| `img_023314` | 66.3% | 0.064% | 53 px |

The pattern is a consistent scale error of 100× to 1000×. On `img_023314` you
masked 66.3% where the true figure is 0.064%.

`img_010196` and `img_018287` genuinely contain no vegetation, so an empty mask
is right there. The other ten need small patches, mostly under 0.25%.

One point that is independent of all this: on `img_004422` your mask crosses the
Lake Powell shoreline and covers open water. **A-8** excludes water from the
mask with no exceptions.

---

## 2. The bigger problem: `uncertain` in a reference set

**This is unchanged from revision 1 and it is still the most consequential
finding.** It has nothing to do with the colour cast.

You used `uncertain` on **38 of 72** presence answers — 53% of the gold set.

| Feature | yes | no | uncertain | Frames that can score an annotator |
|---|---:|---:|---:|---|
| water | 2 | 8 | 2 | 10 / 12 |
| road | 1 | 1 | **10** | **2 / 12** |
| building | 0 | 2 | **10** | **2 / 12** |
| forest | 3 | 2 | 7 | 5 / 12 |
| snow | 0 | 12 | 0 | 12 / 12 |
| field | 3 | 0 | **9** | **3 / 12** |

For a production annotator, `uncertain` is the honest answer when evidence falls
below a rule's minimum. That is what B-0 and G-3 are for and nobody should stop
using it.

**Gold is different, because gold is the answer key.** When the key says
`uncertain`, an annotator answering `yes`, one answering `no`, and one answering
`uncertain` all match it equally well, so the item measures nothing. On road,
building and field this gold set can score annotators on 2, 2 and 3 frames out
of 12 — not enough for a meaningful kappa.

**What to do instead:** commit to whatever the rule's minimum-evidence test
produces, then log the frame and your reasoning in the decision log. The item
stays scoreable, and the log tells us exactly what to revisit if the group later
disagrees. Reserve `uncertain` in gold for images that genuinely cannot support
any answer — rare, not the majority.

---

## 3. Specific calls to revisit

**`img_003522` — building should be `yes`.** You marked `no`. The lower-right
contains an industrial facility: rectangular pads with straight edges and right
angles, and a lined turquoise pond. B-3 is satisfied several times over. This is
the clearest structure anywhere in the gold set.

**`img_004422` — water should be `yes`.** You marked `no`. The lower half
contains large smooth Lake Powell lobes with clean shorelines, filling basins.
Unambiguous under B-1, whose minimum is only ~20 px.

**`img_021152`, `img_022256`, `img_023314` — forest should be `no`.** You marked
`yes` on all three. Corrected, the largest vegetation patch in these frames is
6, 19 and 53 px. B-4 needs continuous canopy larger than a grid cell — roughly
86,000 px. Not close.

**`img_004422`, `img_006404`, `img_018287` — field marked `yes`.** Re-check
against B-10: `field = yes` needs visible agricultural surface — crop colour,
tillage texture, or a centre-pivot circle. Terrain enclosed by tracks does not
qualify.

---

## 4. Exposure and clarity — unchanged

`exposure = over` on 6 of 12 frames: `img_004422`, `img_005564`, `img_006404`,
`img_011104`, `img_022256`, `img_023314`.

The threshold for `over` is clipped highlights on **more than 10%** of the frame.
Across your 12 gold frames the worst clips **0.19%**. Correct answer is `ok` on
all 12. These frames look bright because of haze, not blown highlights.

On clarity you called `img_018287` `moderate` and `img_010196` `clear`, but the
two have nearly identical measured contrast (0.051 and 0.053, the two lowest in
the set). `moderate` was the better call; apply it to both. See rule E-2.

---

## 5. What to redo

1. Read [CHECKPOINT5_REVIEW.md](CHECKPOINT5_REVIEW.md), especially Part 2 and
   the vegetation reference card, and new rules A-13 … A-17.
2. Delete and recreate your three gold projects so they load the corrected
   images:
   ```bash
   python3 scripts/create_label_studio_projects.py --lead-gold --recreate
   ```
   `--recreate` permanently deletes the three existing gold projects and their
   annotations. Upload your current exports to `Sammy_gold_final/` first.
3. Redo all 12 **mask** tasks on the corrected frames. Expect small patches —
   typically well under 0.25% of a frame, and genuinely empty on `img_010196`
   and `img_018287`.
4. Redo all 12 **presence** tasks, replacing `uncertain` with a committed answer
   wherever the minimum-evidence test can decide it. Log anything you must leave
   open.
5. Redo all 12 **quality** tasks with `exposure = ok` throughout, and clarity
   judged by rule E-2.
6. Re-export and re-upload the four files to `Sammy_gold_final/`, same filenames.

Do not look at any A1–A4 submission while redoing this.

**Due: end of July 29**, since A1–A4's calibration scoring depends on it.

---

## 6. A note

Nothing here reflects on your care. Three of the four production annotators made
the same mask mistake independently, which means the instructions and the imagery
were at fault, not the people. The `uncertain` issue is a subtlety about what a
reference set is for that the guide never explained. Both gaps are now written
down as numbered rules.
