from __future__ import annotations

import pathlib

import pytest


@pytest.fixture()
def sandbox_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """A per-test temporary directory to use for file I/O."""
    return tmp_path
