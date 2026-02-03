from __future__ import annotations

import click


@click.command()
def main() -> None:
    """Terrarium command line entrypoint."""
    click.echo("Hello from Terrarium!")
