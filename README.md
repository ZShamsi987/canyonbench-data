# CanyonBench Data

This is the schema, annotation, and release repository for CanyonBench, a geospatially registered benchmark for hallucination and spatial grounding in vision-language models on high-altitude aerial imagery. The separate [CanyonBench code repository](https://github.com/ZShamsi987/canyonbench) contains derivation, registration, inference, and scoring software.

The repository contains no private flight logs, raw video, or source tiles. It
does contain the complete 377-frame public annotation set: 68 Launching and 309
Floating images across 68 trajectory segments and 67 geographic blocks. The
frozen split manifest contains 263 train, 68 validation, and 46 test frames with
no block or segment leakage. Four-coauthor task assignments and public Label
Studio imports are ready; real annotations and registration outputs remain
pending. The capture owner confirmed redistribution rights for annotation
release on 2026-07-26. The official public-domain USGS NAIP reference source is
now frozen and available as a remote QGIS layer plus bounded, checksummed
exports; the final annotation-image license designation remains a release gate.

**First-time annotators start with the
[step-by-step annotator README](annotation/README.md).** It assumes no GitHub,
Python, Docker, or Label Studio experience. Project leads use the
[lead and operations guide](docs/START_ANNOTATING.md). Nobody needs the raw
Google Drive footage: Label Studio reads the curated frames from public GitHub
URLs.

Current sprint assignments are Sammy=`GOLD`, Atharva=`A1`, Pranav G.=`A2`,
Kunsh=`A3`, and Prabhav=`A4`. Qualification is waived for A1-A4 after prior
testing; they start at calibration. The full dataset/training freeze target is
August 20, 2026.

Rebuild the public handoff from the code repository's sampled manifest:

```bash
python3 scripts/prepare_annotation_release.py \
  /path/to/frames_sampled.csv \
  /path/to/frames_named \
  --output .
```

## Release contents

A frozen data release has this shape:

```text
frames/
  launching/                    sampled ascent images (authoritative release)
  floating/                     core scored images
frames_corrected/               colour-corrected copies used for annotation
  launching/                    see metadata/colour_correction.csv
  floating/
masks/
  annotator/                    img_SSSSSS__ID.png
  adjudicated/                  img_SSSSSS.png
labels/
  annotator/{presence,quality,grid,judge_validation}.jsonl
  adjudicated/{presence,quality,grid}.jsonl
registration/
  reference/                    frozen USGS source and remote-first instructions
  points/                       QGIS/canonical control points
  homographies/                 frame-to-reference matrices
  residuals.csv                 held-out metric RMSE and reliability
metadata/
  frames.csv                    master second-indexed join
  provenance.yaml               source, processing, license, and versions
splits/
  splits.csv                    immutable geographic split assignment
```

Public releases may store imagery in a Hugging Face Dataset and metadata here. A Zenodo archive is the citable preservation release. `frames.csv`, content hashes, and split assignments bind those locations together.

## Ground-truth policy

- Label only visible content in `img_SSSSSS.jpg`; never infer from flight location.
- Human annotations are primary. Public geographic data and VARI are weak-label comparisons or annotation aids.
- Green vegetation means visible living green cover, not all vegetation or land-cover class. It is annotated on `frames_corrected/`, where the camera colour cast has been removed; `frames/` remains the authoritative released imagery.
- Feature presence uses exactly water, road/trail, building/structure, dense forest, snow/ice, and cultivated field.
- Grounding is a human-verified 4x4 mask-derived grid and exists only for registration-reliable frames.
- Reliability requires at least six control points, two held out, and held-out RMSE no greater than one quarter of a grid-cell ground width.
- Two coauthors label masks, presence, and quality independently. Conflicts go through adjudication and the append-only decision log.

See the [start guide](docs/START_ANNOTATING.md),
[ANNOTATION.md](ANNOTATION.md), the
[full numbered manual](docs/annotation-manual.md),
[registration contract](docs/registration.md),
[reference-imagery record](registration/reference/README.md),
[current curation status](docs/curation-status.md), and machine-readable
[schemas](schemas).

## Validate before release

With the code repository installed:

```bash
canyonbench validate-release /path/to/frozen-release
```

For schema examples in this repository:

```bash
python scripts/validate_examples.py
```

## Versioning

Data versions use semantic versioning for schemas and release tags. A label-definition, threshold, split, or scoring-population change requires a new minor or major data release. Corrections that do not change the benchmark population may be a patch release but must appear in `CHANGELOG.md`.

## License and citation

Repository documentation, schemas, original annotations, and public annotation
images are governed as described in [LICENSE-DATA.md](LICENSE-DATA.md). Public
access does not imply an unrecorded license grant. Citation placeholders are in
`CITATION.cff` and will be replaced by the frozen DOI and paper record.
