from __future__ import annotations

import pytest


@pytest.fixture()
def temp_workdir(tmp_path):
    """Provide an isolated temporary working directory.

    Returns a `pathlib.Path` created by pytest's built-in `tmp_path` fixture.
    Useful for tests that need to write/read files without affecting the repo.
    """
    return tmp_path
