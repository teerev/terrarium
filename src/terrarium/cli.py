"""Command-line interface for the terrarium package.

This module provides the user-facing entry point for running terrarium simulations.
The initial implementation is a minimal skeleton intended for future expansion.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="terrarium")
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose output.",
)
@click.option(
    "--quiet",
    is_flag=True,
    default=False,
    help="Reduce output.",
)
def main(verbose: bool, quiet: bool) -> None:
    """Terrarium command-line interface.

    Args:
        verbose: Enable verbose output.
        quiet: Reduce output.
    """
    # Placeholder: options are accepted for forward compatibility.
    # Intentionally no behavior yet.
    _ = (verbose, quiet)


@main.command()
@click.option(
    "--steps",
    type=int,
    default=None,
    show_default=False,
    help="Number of simulation steps to run (placeholder).",
)
def run(steps: int | None) -> None:
    """Run a simulation (placeholder).

    Args:
        steps: Number of simulation steps to run.
    """
    # Placeholder no-op.
    _ = steps
