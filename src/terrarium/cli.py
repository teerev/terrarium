from __future__ import annotations

import click

from terrarium import __version__


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="terrarium")
def main() -> None:
    """Terrarium CLI entrypoint."""
    click.echo("Terrarium simulation")
