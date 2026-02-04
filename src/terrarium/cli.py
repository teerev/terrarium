from __future__ import annotations

"""terrarium.cli

The upstream project originally used `typer` for CLI wiring, but this kata
environment does not guarantee that optional CLI dependencies are installed.

This module provides a small stdlib-based CLI that is importable without third
party packages while keeping a compatible `app` object for tests.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from terrarium.io.replay_reader import ReplayReader
from terrarium.render.ascii import render_world_ascii


@dataclass(frozen=True)
class CLIResult:
    exit_code: int = 0


class _ArgparseApp:
    """Tiny adapter exposing a Typer-like testing surface.

    Tests in this repo import `app` from `terrarium.cli` and then use
    typer.testing.CliRunner to invoke it. Typer isn't available here, so we
    provide a compatible `.main(args=..., prog_name=..., standalone_mode=...)`
    hook.
    """

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="terrarium")
        sub = parser.add_subparsers(dest="command", required=True)

        render = sub.add_parser("render", help="Render simulation state")
        render.add_argument(
            "--replay",
            type=str,
            default=None,
            help="Path to a replay JSON file to render",
        )
        render.add_argument(
            "--ascii",
            action="store_true",
            help="Render the world as ASCII",
        )
        render.add_argument(
            "--tick",
            type=int,
            default=None,
            help="Tick to render (defaults to replay start tick)",
        )

        return parser

    def main(
        self,
        args: Optional[List[str]] = None,
        prog_name: Optional[str] = None,
        standalone_mode: bool = True,
    ) -> int:
        parser = self.build_parser()
        if prog_name is not None:
            parser.prog = prog_name

        ns = parser.parse_args(args=args)

        if ns.command == "render":
            return _cmd_render(replay_path=ns.replay, ascii_=bool(ns.ascii), tick=ns.tick)

        # Should be unreachable due to required=True
        return 2


def _cmd_render(*, replay_path: str | None, ascii_: bool, tick: int | None) -> int:
    if not ascii_:
        raise SystemExit("Only --ascii rendering is supported in this environment")

    if replay_path is None:
        raise SystemExit("--replay PATH is required for rendering")

    reader = ReplayReader(Path(replay_path))
    start_tick, _ = reader.tick_range
    t = start_tick if tick is None else int(tick)
    frame = reader.get_frame(t)
    print(render_world_ascii(frame))
    return 0


# Public entrypoint expected by tests
app = _ArgparseApp()


def main() -> None:
    raise SystemExit(app.main())
