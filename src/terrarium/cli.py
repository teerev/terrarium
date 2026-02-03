"""Terrarium command-line interface.

This module provides the public CLI entry point for the terrarium package.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--quiet", is_flag=True, help="Reduce output.")
@click.version_option(__version__, prog_name="terrarium")
def main(verbose: bool, quiet: bool) -> None:
    """Terrarium CLI entry point."""
    # Placeholder for future global logging/verbosity setup.
    # Keep as no-op for the skeleton.
    _ = verbose, quiet


@main.command()
@click.option(
    "--config",
    type=click.Path(exists=False, dir_okay=False, path_type=str),
    help="Path to a configuration file (placeholder).",
)
def run(config: str | None) -> None:
    """Run a simulation (placeholder)."""
    _ = config
    # Placeholder: no simulation execution yet.
    raise SystemExit(0)
