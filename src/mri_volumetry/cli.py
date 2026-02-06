from __future__ import annotations

import argparse
from pathlib import Path

from mri_volumetry.logging_utils import setup_logging
from mri_volumetry.pipeline import run_pipeline


def main() -> None:
    setup_logging()

    parser = argparse.ArgumentParser(description="MRI brain volumetry pipeline (MVP)")
    parser.add_argument("--input", type=Path, required=True, help="Path to T1 NIfTI (.nii/.nii.gz)")
    parser.add_argument("--outdir", type=Path, required=True, help="Output directory")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    run_pipeline(input_path=args.input, outdir=args.outdir)
