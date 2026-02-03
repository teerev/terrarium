"""Terrarium command-line interface.

This module provides the user-facing CLI entry point for running terrarium
simulations.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "--version", prog_name="terrarium")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--quiet", is_flag=True, help="Suppress non-error output.")
def main(verbose: bool, quiet: bool) -> None:
    """Terrarium CLI entry point."""
    if verbose and quiet:
        raise click.UsageError("--verbose and --quiet are mutually exclusive")


@main.command()
@click.option("--steps", type=int, default=0, show_default=True, help="Simulation steps.")
def run(steps: int) -> None:
    """Run a simulation (placeholder)."""
    _ = steps
    return None
