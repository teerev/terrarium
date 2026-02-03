from click.testing import CliRunner

from terrarium import __version__
from terrarium.cli import main


def test_cli_help_exits_zero():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Terrarium command line interface" in result.output or "Terrarium" in result.output


def test_cli_version_output():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_run_subcommand_exists():
    runner = CliRunner()
    result = runner.invoke(main, ["run", "--help"])
    assert result.exit_code == 0
    assert "Run a simulation" in result.output
