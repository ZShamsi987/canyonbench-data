---
pretty_name: CanyonBench
language:
  - en
task_categories:
  - visual-question-answering
  - image-classification
  - image-segmentation
tags:
  - aerial-imagery
  - hallucination
  - spatial-grounding
  - vision-language-models
license: other
---

# Dataset card for CanyonBench

## Summary

CanyonBench evaluates whether vision-language models faithfully describe visible content in high-altitude balloon imagery. Primary tasks are six-feature presence classification, green-visible-vegetation percentage estimation, 4x4 vegetation grounding on registration-reliable frames, and false-premise correction. Free description is secondary.

This repository is in curation. Automated preprocessing retained 377 sampled frames: 68 Launching and 309 Floating, grouped into 68 bounded trajectory segments and 67 geographic blocks. The frozen split manifest contains 263 train, 68 validation, and 46 test frames with no block or segment leakage. The imagery is not yet public, and annotator agreement, registration success, source-license clearance, full privacy review, and DOI remain unset until the human and release gates pass.

## Dataset structure

Each image key is its rounded flight elapsed second: `img_SSSSSS.jpg`. `metadata/frames.csv` joins the image to flight phase, GPS, altitude, movement, segment, geographic split, objective quality controls, human labels, mask cover, registration status, and held-out error.

The core scored population is Floating. Launching supports the ascent-trajectory association analysis. Ground and Initializing are excluded because they are not aerial and may show identifiable people. Terminating is archived but not scored.

## Annotation

Two coauthors independently label each gold frame. Green-visible-vegetation masks are binary, full-resolution PNGs. Presence and condition values are constrained categorical JSONL records. A 30-frame shared set monitors agreement and a 12-frame gold qualification set gates production. Ambiguities enter an append-only decision log; new rulings are numbered and applied retrospectively at adjudication.

Target agreement is Dice >= 0.75 for masks and kappa >= 0.6 for presence and quality. Actual measurements will be published per release.

## Registration

Frame-to-reference homographies use stable point correspondences and a metric reference CRS. At least six points are placed, with two held out. Held-out reprojection RMSE is compared with `ground_width_m / 16`, one quarter of a 4x4 grid-cell width. Only reliable frames enter grounding evaluation. Reprojection errors and exclusions are published rather than hidden.

## Splits and correlation

The one-frame-per-second archive is not the evaluation population. Frames are deduplicated with a 60-second minimum interval plus 500-metre movement and perceptual-change thresholds. Trajectory segments are bounded to ten minutes and refined at geographic split boundaries. Each geographic block and resulting segment belongs to exactly one split. Statistical intervals resample segments, never individual frames.

## Intended uses

- benchmark visible-feature hallucination in general and remote-sensing VLMs;
- compare neutral and evidence-first structured prompting;
- analyze altitude/effective-resolution associations with quality and prevalence controls;
- study grid-based grounding on the validated registration subset.

The dataset evaluates perception and evidence localization. It is not validated for autonomous navigation, emergency response, land-management decisions, surveillance, or claims about causal altitude effects.

## Limitations and risks

Altitude covaries with location, flight stage, footprint, haze, exposure, and scene content. Registration uses a planar approximation despite canyon relief. Green-visible vegetation excludes dry vegetation and sub-resolution tint. Human labels can remain uncertain. Source imagery and flight coverage represent one region and acquisition context. Models may exploit visual or geographic priors even when prompts forbid them.

## Personal and sensitive information

Ground and Initializing frames are excluded. Before release, sampled frames are reviewed for identifiable people, vehicles, private information, and source-license constraints. Annotator ids in public records are stable pseudonymous initials, not contact details.

## Provenance and licensing

Each release publishes capture and processing provenance, hashes, code commit, public-layer versions/dates, and per-source licensing. Public layers do not define per-frame truth. See `metadata/provenance.yaml` and `LICENSE-DATA.md`.

## Citation

Use the DOI and paper citation after the first frozen release. Until then, cite the software and versioned repository commit; do not cite this pre-data repository as a completed benchmark dataset.
