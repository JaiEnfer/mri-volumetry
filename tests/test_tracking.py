from pathlib import Path

from mri_volumetry.pipeline import run_pipeline


def test_pipeline_runs_and_logs(tmp_path: Path) -> None:
    run_info = run_pipeline(tmp_path)
    assert run_info.run_id

    mlruns_dir = tmp_path / "mlruns"
    assert mlruns_dir.exists()
