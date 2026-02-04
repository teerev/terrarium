"""Command-line interface for the Terrarium project.

This module provides the user-facing CLI entry point for running simulations.
"""

from __future__ import annotations

import click

from terrarium import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="terrarium")
def main() -> None:
    """Main CLI entry point for the `terrarium` command."""


@main.command()
def run() -> None:
    """Run a simulation (placeholder; no-op)."""

