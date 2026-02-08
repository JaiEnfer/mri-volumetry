from __future__ import annotations

from pathlib import Path

import mlflow


def setup_mlflow(tracking_dir: Path) -> None:
    """
    Configure MLflow to log experiments locally.

    Why local tracking?
    - Easy to use on Windows
    - Works offline
    - Can be swapped later for a remote MLflow server
    """
    tracking_uri = tracking_dir.resolve().as_uri()
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("brain-mri-volumetry")


def log_basic_run(run_id: str) -> None:
    """
    Log a minimal MLflow run.

    This proves:
    - MLflow is wired correctly
    - We can attach metadata to pipeline runs
    """
    with mlflow.start_run(run_name=run_id):
        mlflow.log_param("project", "brain_mri_volumetry")
        mlflow.log_param("run_id", run_id)

        # Dummy metric for now
        mlflow.log_metric("pipeline_stage", 1.0)
