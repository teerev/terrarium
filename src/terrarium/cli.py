"""Command-line interface for the terrarium package.

This module provides the user-facing CLI entry point.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "--version", "-V")
def main() -> None:
    """Terrarium command line interface."""


@main.command()
@click.option(
    "--verbose/--quiet",
    default=False,
    help="Enable verbose output (or quiet mode). Placeholder for now.",
)
def run(verbose: bool) -> None:
    """Run a simulation (placeholder).

    This is currently a no-op skeleton command.
    """

    # Placeholder behavior: succeed without doing anything.
    # Keep parameter to reserve the CLI surface for future use.
    _ = verbose
