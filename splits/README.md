# Geographic splits

`splits.csv` is generated once from sampled frames using geographic blocks and whole trajectory segments. After model development starts, it is immutable within a data release. Any population or split change requires a new data version and leakage validation.

Current curation population: 377 frames in 68 trajectory segments and 67 blocks.
The deterministic assignment contains 263 train, 68 validation, and 46 test
frames. Automated validation found zero segment or block leakage.
