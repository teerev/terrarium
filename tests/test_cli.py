from __future__ import annotations

from click.testing import CliRunner

from terrarium.cli import app


def test_cli_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "save" in result.output
    assert "load" in result.output
