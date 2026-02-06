from __future__ import annotations

from pathlib import Path

import nibabel as nib


def load_nifti(path: Path) -> nib.Nifti1Image:
    if not path.exists():
        raise FileNotFoundError(path)
    img = nib.load(str(path))
    if not isinstance(img, nib.Nifti1Image):
        raise TypeError("Expected a NIfTI1 image.")
    return img
