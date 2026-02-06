from __future__ import annotations

import json
import logging
import platform
from datetime import datetime, timezone
from pathlib import Path

from mri_volumetry.io import load_nifti
from mri_volumetry.metrics import compute_volumes_ml
from mri_volumetry.segment import dummy_tissue_segmentation

logger = logging.getLogger(__name__)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_pipeline(input_path: Path, outdir: Path) -> None:
    logger.info("Starting pipeline")
    logger.info("Input: %s", input_path)

    logger.info("Loading NIfTI")
    img = load_nifti(input_path)

    logger.info("Running segmentation (placeholder)")
    seg = dummy_tissue_segmentation(img)

    logger.info("Computing volumes")
    metrics = compute_volumes_ml(seg, img)

    logger.info("Writing outputs")
    (outdir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    run_info = {
        "timestamp_utc": _utc_now_iso(),
        "input": str(input_path),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    (outdir / "run.json").write_text(json.dumps(run_info, indent=2), encoding="utf-8")

    logger.info("Done. Wrote metrics.json and run.json to %s", outdir)
