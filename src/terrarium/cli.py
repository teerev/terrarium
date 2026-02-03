from __future__ import annotations

import json
from pathlib import Path

import click

from terrarium.io.persistence import load_snapshot, save_snapshot
from terrarium.io.snapshot import restore_snapshot


@click.group()
def app() -> None:
    """Terrarium command line interface."""


@app.command("save")
@click.option("--output", "output_path", required=True, type=click.Path(dir_okay=False, path_type=Path))
def save_cmd(output_path: Path) -> None:
    """Save a snapshot JSON file.

    Minimal CLI: loads snapshot JSON from stdin if provided as full payload.
    (A running simulation integration is out of scope for this repo version.)
    """

    try:
        # Expect a snapshot payload on stdin if piped; otherwise refuse.
        if click.get_text_stream("stdin").isatty():
            raise click.ClickException(
                "No snapshot provided on stdin. Pipe a snapshot JSON payload into this command."
            )
        data = json.load(click.get_text_stream("stdin"))
        save_snapshot(data, output_path)
    except click.ClickException:
        raise
    except Exception as e:
        raise click.ClickException(str(e)) from e


@app.command("load")
@click.option("--input", "input_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def load_cmd(input_path: Path) -> None:
    """Load a snapshot JSON file and validate it.

    For now, prints basic info as JSON to stdout.
    """

    try:
        snap = load_snapshot(input_path)
        # Validate restorable.
        world, rng = restore_snapshot(snap)
        info = {
            "tick": int(world.tick),
            "grid": {"width": int(world.grid.width), "height": int(world.grid.height)},
            "rng_seed": int(rng.seed),
        }
        click.echo(json.dumps(info, indent=2, sort_keys=True))
    except Exception as e:
        raise click.ClickException(str(e)) from e
