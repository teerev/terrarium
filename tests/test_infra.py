from __future__ import annotations

import pathlib


def test_sanity_check() -> None:
    assert 1 + 1 == 2


def test_fixture_available(sandbox_dir: pathlib.Path) -> None:
    assert sandbox_dir.exists()
    assert sandbox_dir.is_dir()
