from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """
    Central place for project paths.

    Why:
    - Avoid hardcoding "data/..." all over the codebase.
    - Makes it easy to change folder layout later.
    """

    root: Path
    data_dir: Path
    models_dir: Path
    reports_dir: Path

    @staticmethod
    def from_repo_root(root: Path | None = None) -> ProjectPaths:
        """
        Create paths assuming the current working directory is the repo root.

        If you run scripts from the repo root (recommended), this will work
        consistently on Windows/macOS/Linux.
        """
        root = root or Path.cwd()
        return ProjectPaths(
            root=root,
            data_dir=root / "data",
            models_dir=root / "models",
            reports_dir=root / "reports",
        )
