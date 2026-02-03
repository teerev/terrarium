from __future__ import annotations

from click.testing import CliRunner

from terrarium.cli import main


def test_cli_default_name() -> None:
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_cli_custom_name() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--name", "Terrarium"])
    assert result.exit_code == 0
    assert "Hello, Terrarium!" in result.output
