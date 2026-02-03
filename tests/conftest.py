from __future__ import annotations

import pathlib

import pytest


@pytest.fixture
def sandbox_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """A temporary directory intended for file I/O tests.

    This fixture is composable: tests can create files within it or pass it to
    helpers expecting a writable directory.
    """

    return tmp_path
