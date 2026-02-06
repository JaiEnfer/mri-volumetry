from __future__ import annotations

from typing import Any

import nibabel as nib
import numpy as np


def _voxel_volume_ml(img: nib.Nifti1Image) -> float:
    zooms = img.header.get_zooms()[:3]  # voxel spacing in mm
    voxel_mm3 = float(zooms[0] * zooms[1] * zooms[2])
    return voxel_mm3 / 1000.0  # 1000 mm^3 = 1 ml


def compute_volumes_ml(seg: np.ndarray, img: nib.Nifti1Image) -> dict[str, Any]:
    vv = _voxel_volume_ml(img)

    labels = {"gm_ml": 1, "wm_ml": 2, "csf_ml": 3}
    out: dict[str, Any] = {}

    for name, lab in labels.items():
        vox = int(np.sum(seg == lab))
        out[name] = vox * vv

    out["brain_ml"] = out["gm_ml"] + out["wm_ml"] + out["csf_ml"]
    return out
