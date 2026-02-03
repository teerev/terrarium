from __future__ import annotations

import terrarium


def test_version_is_string() -> None:
    assert isinstance(terrarium.__version__, str)
