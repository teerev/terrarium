from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    """Path to the repository root (parent of the tests/ directory)."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def tmp_workdir(tmp_path: Path) -> Path:
    """A dedicated temporary working directory for tests that do file I/O."""
    workdir = tmp_path / "workdir"
    workdir.mkdir(parents=True, exist_ok=True)
    return workdir
