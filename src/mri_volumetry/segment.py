from __future__ import annotations

import nibabel as nib
import numpy as np


def dummy_tissue_segmentation(img: nib.Nifti1Image) -> np.ndarray:
    """
    MVP placeholder segmentation.
    Labels:
      0 = background
      1 = GM
      2 = WM
      3 = CSF

    NOT clinically valid. This is only to test pipeline wiring.
    """
    data = img.get_fdata(dtype=np.float32)
    data = (data - float(data.min())) / (float(data.max()) - float(data.min()) + 1e-8)

    seg = np.zeros(data.shape, dtype=np.uint8)
    seg[data > 0.35] = 1
    seg[data > 0.55] = 2
    seg[(data > 0.15) & (data <= 0.35)] = 3
    return seg
