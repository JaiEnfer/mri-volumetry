from __future__ import annotations

import json
from pathlib import Path

import nibabel as nib
import numpy as np
from mri_volumetry.pipeline import run_pipeline


def test_pipeline_creates_metrics(tmp_path: Path) -> None:
    data = np.zeros((16, 16, 16), dtype=np.float32)
    data[4:12, 4:12, 4:12] = 100.0
    affine = np.eye(4, dtype=np.float32)

    img = nib.Nifti1Image(data, affine)
    in_path = tmp_path / "t1.nii.gz"
    nib.save(img, str(in_path))

    outdir = tmp_path / "out"
    outdir.mkdir()

    run_pipeline(in_path, outdir)

    metrics_path = outdir / "metrics.json"
    assert metrics_path.exists()

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert "brain_ml" in metrics
    assert metrics["brain_ml"] > 0
