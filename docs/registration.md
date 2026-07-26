# Registration record contract

The frozen reference is 2023 USGS NAIP, streamed from the official ImageServer;
see [`registration/reference/README.md`](../registration/reference/README.md).
Use `EPSG:26912` (NAD83 / UTM zone 12N) for all published map coordinates.
The source is public domain and its exact service, catalog audit, terms, and
acknowledgment are recorded in `registration/reference/source.yaml`.

Each control-point file contains frame pixel coordinates (`image_x`, `image_y`), projected metric reference coordinates (`map_x`, `map_y`), and a role (`fit` or `holdout`). Save the reference CRS and imagery provenance alongside the batch manifest. Never compute “metres” from longitude/latitude degrees.

Use at least six total points and aim for eight. Four or more fit points determine the projective homography; exactly two or more held-out points measure generalization error. Points must cover every quadrant and include a central point. Avoid shadow/cloud edges, changing water lines, vehicles, and ambiguous smooth curves.

`registration/residuals.csv` publishes total, fit, and held-out counts; held-out RMSE; the per-frame threshold; and reliability. Matrices go in `registration/homographies/img_SSSSSS.homography.json` and map frame pixels to the documented reference coordinate system.

## Exact QGIS setup

1. Choose **Layer → Add Layer → Add ArcGIS REST Server Layer**.
2. Create a connection named `USGS NAIP` using the ImageServer URL from
   `source.yaml`, connect, and add `USGSNAIPImagery`.
3. Set the project CRS to `EPSG:26912`.
4. Open **Layer → Georeferencer**, load the CanyonBench frame as the source,
   and set transformation type to **Projective** and target CRS to
   `EPSG:26912`.
5. Use the frame GPS only as a starting search point. Match stable, point-like
   landmarks visible in both the oblique/high-altitude frame and NAIP.
6. Place at least eight candidate pairs when possible. Assign at least six
   well-distributed points to `fit` and at least two to `holdout`.
7. Export the canonical control-point CSV with
   `image_x,image_y,map_x,map_y,role`. Do not rely only on QGIS's private
   project state.
8. Run the code repository's `canyonbench register` command, inspect held-out
   errors, and keep grounding only when the documented reliability gate passes.

QGIS streams the live map. When a bounded raster must be frozen, use
`canyonbench reference-chip`; preserve its generated provenance sidecar and
SHA-256, but keep the large GeoTIFF in the ignored local cache.

A frame is reliable when `holdout_rmse_m <= ground_width_m / 16`. If point placement or fit fails, include a residual record with reliability false when representable, omit the grounding annotation, and preserve the visible-image presence/mask labels.
