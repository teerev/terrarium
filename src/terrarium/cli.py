"""Command-line interface for Terrarium.

This module provides the user-facing entry point for running simulations.
Currently, it includes a placeholder command set to establish a stable CLI
surface area for future expansion.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="terrarium")
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--quiet", is_flag=True, help="Suppress non-error output.")
def main(verbose: bool, quiet: bool) -> None:
    """Terrarium command-line interface."""
    if verbose and quiet:
        raise click.UsageError("--verbose and --quiet are mutually exclusive")


@main.command()
@click.option(
    "--steps",
    type=int,
    default=0,
    show_default=True,
    help="Number of simulation steps to run (placeholder).",
)
def run(steps: int) -> None:
    """Run a simulation (placeholder)."""
    # No-op placeholder for now.
    _ = steps


if __name__ == "__main__":
    main()
