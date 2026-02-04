from __future__ import annotations

from terrarium.cli import app


def test_cli_app_importable() -> None:
    # The kata environment does not include third-party CLI libs.
    # Ensure the CLI module remains importable and exposes an `app`.
    assert app is not None
