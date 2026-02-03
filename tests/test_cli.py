from __future__ import annotations

from terrarium.cli import app


def test_cli_app_importable() -> None:
    assert app is not None
