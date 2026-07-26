# Pre-release audit record

Complete this document for each frozen release.

## Identity

- Release version:
- Code commit:
- Data commit:
- Prepared by:
- Review date:

## Sources and licenses

- [ ] Private source checksums recorded
- [ ] Camera/video redistribution rights confirmed
- [ ] Reference imagery product, date, and license recorded
- [ ] Geographic layer product, vintage, resolution, and license recorded
- [ ] No source is implicitly relicensed

## Privacy and integrity

- [ ] Ground and Initializing frames absent
- [ ] Frames reviewed for identifiable people and sensitive information
- [ ] Image/mask dimensions and binary values pass
- [ ] Filename/elapsed-second joins pass
- [ ] Zero-GPS records absent
- [ ] Content checksums frozen

## Annotation and registration

- [ ] Qualification pass or documented prior-test waiver, plus midpoint drift
      checks, complete
- [ ] Dice and kappa reported
- [ ] Decision log adjudicated and applied retrospectively
- [ ] Held-out registration residuals recomputed
- [ ] Unreliable frames have no grounding records
- [ ] Grid overrides are logged
- [ ] VARI was calibrated only on the calibration split

## Evaluation population

- [ ] Sampling configuration frozen
- [ ] Raw and retained counts reported
- [ ] Segment count reported
- [ ] Geographic block and segment leakage checks pass
- [ ] Split file frozen before benchmark inference

## Publication

- [ ] Dataset card contains actual counts and limitations
- [ ] Both repositories cross-link exact versions
- [ ] Hugging Face artifacts match hashes
- [ ] Zenodo archive and DOI verified
- [ ] Citation records updated
