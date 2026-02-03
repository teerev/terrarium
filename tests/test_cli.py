from click.testing import CliRunner

from terrarium.cli import main


def test_cli_runs() -> None:
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "Hello from Terrarium!" in result.output
