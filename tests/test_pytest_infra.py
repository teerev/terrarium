from __future__ import annotations

from pathlib import Path


def test_tmp_workdir_fixture_creates_directory(tmp_workdir: Path) -> None:
    assert tmp_workdir.exists()
    assert tmp_workdir.is_dir()


def test_project_root_fixture_points_to_repo_root(project_root: Path) -> None:
    # Basic smoke check: repository root should contain pyproject.toml
    assert (project_root / "pyproject.toml").exists()
