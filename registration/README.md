# Registration artifacts

`points/` stores frame-to-reference correspondences, `homographies/` stores image-to-map matrices, and `residuals.csv` publishes held-out errors and reliability. Real artifacts are absent from the pre-data release.

`reference/` freezes the official USGS NAIP source, public-domain terms,
catalog audit, CRS, and storage policy. Operators stream the source in QGIS and
download only bounded chips when a match must be frozen; full source tiles do
not belong in Git.
