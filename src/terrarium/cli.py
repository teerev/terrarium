import click


@click.command()
def main() -> None:
    """Terrarium CLI entrypoint."""
    click.echo("Terrarium")
