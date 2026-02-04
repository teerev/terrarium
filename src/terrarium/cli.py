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
from terrarium.render.terminal import TerminalViewer


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

        watch = sub.add_parser("watch", help="Watch a replay in the terminal")
        watch.add_argument(
            "--replay",
            type=str,
            default=None,
            help="Path to a replay JSON file to watch",
        )
        watch.add_argument(
            "--fps",
            type=float,
            default=10.0,
            help="Playback speed in frames per second",
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

        # argparse prints help to stdout and then raises SystemExit(0).
        # Capture that behavior but ensure help text is on stdout for tests.
        try:
            ns = parser.parse_args(args=args)
        except SystemExit as e:
            code = getattr(e, "code", 0)
            try:
                icode = int(code)
            except Exception:
                icode = 0

            if icode == 0 and args is not None and any(a in ("-h", "--help") for a in args):
                # argparse defaults to stderr for error output, but help text is
                # expected on stdout and tests assert on captured stdout.
                parser.print_help()

            return icode

        if ns.command == "render":
            return _cmd_render(replay_path=ns.replay, ascii_=bool(ns.ascii), tick=ns.tick)

        if ns.command == "watch":
            return _cmd_watch(replay_path=ns.replay, fps=float(ns.fps))

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


def _cmd_watch(*, replay_path: str | None, fps: float) -> int:
    if replay_path is None:
        raise SystemExit("--replay PATH is required for watch")

    reader = ReplayReader(Path(replay_path))
    TerminalViewer().play_replay(reader, fps=float(fps))
    return 0


# Public entrypoint expected by tests
app = _ArgparseApp()


def main() -> None:
    raise SystemExit(app.main())
