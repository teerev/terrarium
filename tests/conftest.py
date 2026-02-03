from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    """A writable temporary directory for filesystem-based tests."""

    p = tmp_path / "sandbox"
    p.mkdir()
    return p
