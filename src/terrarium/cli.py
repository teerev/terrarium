from __future__ import annotations

import click


@click.command()
@click.option("--name", default="World", help="Name to greet")
def main(name: str) -> None:
    """Terrarium CLI entrypoint."""

    click.echo(f"Hello, {name}!")
