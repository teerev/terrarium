from __future__ import annotations


def test_cli_importable() -> None:
    from terrarium.cli import main

    assert callable(main)
