import click


@click.command()
def main() -> None:
    """Terrarium CLI entry point."""
    click.echo("Hello from Terrarium!")
