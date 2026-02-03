from click.testing import CliRunner

from terrarium import __version__
from terrarium.cli import main


def test_cli_help_exits_zero() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Terrarium command-line interface" in result.output


def test_cli_version_output() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_run_subcommand_exists() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run a simulation" in result.output
