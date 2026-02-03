from __future__ import annotations

from pathlib import Path


def test_sanity_check() -> None:
    assert True


def test_fixture_available(sandbox: Path) -> None:
    assert sandbox.exists()
    assert sandbox.is_dir()
