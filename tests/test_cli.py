from __future__ import annotations

from click.testing import CliRunner

from terrarium.cli import main


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Terrarium" in result.output


def test_cli_version_output() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "terrarium" in result.output
