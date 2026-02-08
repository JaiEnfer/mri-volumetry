from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class ScanRecord:
    """
    One row in our dataset manifest.

    We keep it simple:
    - subject_id: who the scan belongs to
    - session_id: timepoint (baseline/follow-up), if we can infer it
    - modality: e.g. T1w
    - path: where the NIfTI file is on disk
    """

    subject_id: str
    session_id: str
    modality: str
    path: str


def _guess_subject_and_session(file_path: Path) -> tuple[str, str]:
    """
    Best-effort parsing of subject + session from folders/filename.

    OASIS comes in different “layouts” depending on which OASIS subset you downloaded.
    So we make this robust and conservative:
    - If we can’t infer session, we use "ses-unknown"
    - If we can’t infer subject, we fallback to the parent folder name
    """
    text = str(file_path).lower()

    # Common patterns like "sub-0001", "oasis1_0001", etc.
    subj_match = re.search(r"(sub-\w+|oasis\w*[_-]\d+|\d{3,})", text)
    subject_id = subj_match.group(1) if subj_match else file_path.parent.name

    # Common timepoint/session indicators
    ses_match = re.search(r"(ses-\w+|timepoint-\d+|tp\d+|visit-\d+)", text)
    session_id = ses_match.group(1) if ses_match else "ses-unknown"

    # Normalize to avoid weird characters
    subject_id = re.sub(r"[^a-z0-9_-]+", "", subject_id)
    session_id = re.sub(r"[^a-z0-9_-]+", "", session_id)

    return subject_id, session_id


def build_manifest(raw_oasis_dir: Path) -> pd.DataFrame:
    """
    Scan the raw OASIS directory for NIfTI files and produce a manifest table.
    """
    nii_files = sorted(list(raw_oasis_dir.rglob("*.nii")) + list(raw_oasis_dir.rglob("*.nii.gz")))
    records: list[ScanRecord] = []

    for fp in nii_files:
        subject_id, session_id = _guess_subject_and_session(fp)

        # crude modality guess: if filename contains "t1" assume T1w else unknown
        modality = "T1w" if "t1" in fp.name.lower() else "unknown"

        records.append(
            ScanRecord(
                subject_id=subject_id,
                session_id=session_id,
                modality=modality,
                path=str(fp.resolve()),
            )
        )

    df = pd.DataFrame([r.__dict__ for r in records])
    return df


def main() -> None:
    repo_root = Path.cwd()
    raw_dir = repo_root / "data" / "raw" / "oasis"
    out_path = repo_root / "data" / "processed" / "manifest.csv"

    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw OASIS directory not found: {raw_dir}")

    df = build_manifest(raw_dir)

    # Save even if empty (helps debugging), but print a warning
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

    print(f"Found {len(df)} NIfTI files.")
    print(f"Wrote manifest to: {out_path}")
    if len(df) > 0:
        print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
