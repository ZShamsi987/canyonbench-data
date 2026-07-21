# CanyonBench Data

This is the schema, annotation, and release repository for CanyonBench, a geospatially registered benchmark for hallucination and spatial grounding in vision-language models on high-altitude aerial imagery. The separate [CanyonBench code repository](https://github.com/ZShamsi987/canyonbench) contains derivation, registration, inference, and scoring software.

The repository intentionally contains no recovered flight logs, raw video, extracted frames, reference tiles, or real annotations yet. Those inputs will be added only after source checks, annotation, registration validation, privacy review, and release validation. Small example records document every contract without pretending placeholder labels are ground truth.

## Release contents

A frozen data release has this shape:

```text
frames/
  launching/                    sampled ascent images
  floating/                     core scored images
masks/
  annotator/                    img_SSSSSS__ID.png
  adjudicated/                  img_SSSSSS.png
labels/
  annotator/{presence,quality,grid,judge_validation}.jsonl
  adjudicated/{presence,quality,grid}.jsonl
registration/
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
- Green vegetation means visible living green cover, not all vegetation or land-cover class.
- Feature presence uses exactly water, road/trail, building/structure, dense forest, snow/ice, and cultivated field.
- Grounding is a human-verified 4x4 mask-derived grid and exists only for registration-reliable frames.
- Reliability requires at least six control points, two held out, and held-out RMSE no greater than one quarter of a grid-cell ground width.
- Two coauthors label masks, presence, and quality independently. Conflicts go through adjudication and the append-only decision log.

See [ANNOTATION.md](ANNOTATION.md), the [full numbered manual](docs/annotation-manual.md), [registration contract](docs/registration.md), and machine-readable [schemas](schemas).

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

Repository documentation, schemas, and original annotations are licensed as described in [LICENSE-DATA.md](LICENSE-DATA.md). Future image files retain the terms recorded for their source; no image is released until that audit is complete. Citation placeholders are in `CITATION.cff` and will be replaced by the frozen DOI and paper record.
