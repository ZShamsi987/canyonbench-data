# CanyonBench registration reference

The selected reference is the official **USGS NAIP Imagery** ArcGIS
ImageServer. It is public domain, covers every sampled World-10 GPS location,
and supplies 2023 Arizona natural-color imagery at 0.3 metre nominal
resolution. The exact machine-readable record is in
[`source.yaml`](source.yaml).

## Use it without downloading the route

1. Open QGIS.
2. Choose **Layer → Add Layer → Add ArcGIS REST Server Layer**.
3. Create a connection named `USGS NAIP` with this URL:
   `https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer`
4. Connect and add `USGSNAIPImagery`.
5. Set the project CRS to **EPSG:26912 — NAD83 / UTM zone 12N**.
6. Use the frame's `lat` and `lon` from `metadata/frames_sampled.csv` only as
   the starting search location. The camera view need not be centered directly
   below the balloon.
7. Add control points according to
   [`docs/registration.md`](../../docs/registration.md).

QGIS streams only the visible area. If a registration operator must save an
exact local GeoTIFF, use the code repository's `canyonbench reference-chip`
command after finding the matching WGS84 extent. Store the chip under ignored
`work/reference/`, and retain its generated `*.reference.json` checksum
sidecar with the registration working record.

Do **not** download or commit all 189 full-resolution tiles. Git contains the
source contract, requests, checksums, points, matrices, and residuals; USGS
remains the canonical raster host.

Requested acknowledgment:

> Map services and data available from U.S. Geological Survey, National
> Geospatial Program.
