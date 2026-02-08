from src.mri_volumetry.pipeline import create_run_info


def test_create_run_info_has_values() -> None:
    info = create_run_info()
    assert info.run_id  # non-empty
    assert "T" in info.created_utc  # ISO timestamps contain 'T' (e.g., 2026-02-08T...)
