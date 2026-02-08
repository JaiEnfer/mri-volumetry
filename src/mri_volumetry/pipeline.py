from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from mri_volumetry.tracking import log_basic_run, setup_mlflow


@dataclass(frozen=True)
class PipelineRunInfo:
    run_id: str
    created_utc: str


def create_run_info() -> PipelineRunInfo:
    now = datetime.now(timezone.utc)
    run_id = now.strftime("%Y%m%d-%H%M%S")
    created_utc = now.isoformat()
    return PipelineRunInfo(run_id=run_id, created_utc=created_utc)


def run_pipeline(root_dir: Path) -> PipelineRunInfo:
    """
    Entry point for the pipeline.

    For now:
    - Create run metadata
    - Log it to MLflow
    """
    run_info = create_run_info()

    mlflow_dir = root_dir / "mlruns"
    setup_mlflow(mlflow_dir)
    log_basic_run(run_info.run_id)

    return run_info
