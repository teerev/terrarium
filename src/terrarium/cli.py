"""Command-line interface for Terrarium.

This module defines the user-facing CLI entrypoint exposed as the `terrarium`
console script.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--quiet", is_flag=True, help="Reduce output.")
@click.version_option(__version__, "--version", prog_name="terrarium")
def main(verbose: bool, quiet: bool) -> None:
    """Terrarium command line interface."""
    if verbose and quiet:
        raise click.UsageError("--verbose and --quiet are mutually exclusive")


@main.command()
def run() -> None:
    """Run a terrarium simulation (placeholder)."""
    # Placeholder for future simulation execution.
    return
