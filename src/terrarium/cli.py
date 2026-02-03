from __future__ import annotations

import argparse
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="terrarium")
    sub = parser.add_subparsers(dest="command")

    export = sub.add_parser("export-replay", help="Export a simulation replay to JSON")
    export.add_argument("--output", "-o", required=True, type=Path, help="Output replay JSON path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "export-replay":
        # Minimal CLI surface: exporting requires a live simulation object.
        # The project currently does not define a standard way to load/run a
        # simulation from CLI arguments, so we provide a clear error.
        parser.error("export-replay requires an in-process Simulation object; use terrarium.io.export_replay(sim, path) from Python")

    parser.print_help()
    return 0
