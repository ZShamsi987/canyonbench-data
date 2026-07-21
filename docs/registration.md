# Registration record contract

Each control-point file contains frame pixel coordinates (`image_x`, `image_y`), projected metric reference coordinates (`map_x`, `map_y`), and a role (`fit` or `holdout`). Save the reference CRS and imagery provenance alongside the batch manifest. Never compute “metres” from longitude/latitude degrees.

Use at least six total points and aim for eight. Four or more fit points determine the projective homography; exactly two or more held-out points measure generalization error. Points must cover every quadrant and include a central point. Avoid shadow/cloud edges, changing water lines, vehicles, and ambiguous smooth curves.

`registration/residuals.csv` publishes total, fit, and held-out counts; held-out RMSE; the per-frame threshold; and reliability. Matrices go in `registration/homographies/img_SSSSSS.homography.json` and map frame pixels to the documented reference coordinate system.

A frame is reliable when `holdout_rmse_m <= ground_width_m / 16`. If point placement or fit fails, include a residual record with reliability false when representable, omit the grounding annotation, and preserve the visible-image presence/mask labels.

