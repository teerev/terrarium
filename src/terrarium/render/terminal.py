from __future__ import annotations

import os
import select
import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

from terrarium.render.ascii import render_world_ascii


_CLEAR = "\x1b[2J\x1b[H"
_HIDE_CURSOR = "\x1b[?25l"
_SHOW_CURSOR = "\x1b[?25h"


def _world_tick(world: Any) -> int | None:
    t = getattr(world, "tick", None)
    if isinstance(world, dict):
        t = world.get("tick", t)
    try:
        return None if t is None else int(t)
    except Exception:
        return None


def _population(world: Any) -> int:
    # For snapshots/replays we have a flat entity list.
    if isinstance(world, dict):
        ents = world.get("entities")
        if isinstance(ents, list):
            return sum(1 for e in ents if isinstance(e, dict) and e.get("type") == "organism")
        return 0

    # For WorldState, entities live in an internal dict.
    ents2 = getattr(world, "_entities", None)
    if isinstance(ents2, dict):
        n = 0
        for e in ents2.values():
            et = getattr(e, "entity_type", None)
            v = getattr(et, "value", et)
            if str(v) == "organism":
                n += 1
        return n

    return 0


@dataclass(slots=True)
class TerminalViewer:
    """Simple terminal-based viewer.

    Controls (when stdin is a TTY):
    - space: pause/resume
    - s: step one frame when paused
    - q: quit

    In non-interactive contexts (stdin not a TTY), controls are disabled and the
    viewer simply plays frames at the requested FPS.
    """

    organism_char: str = "O"
    resource_char: str = "*"
    empty_char: str = "."

    def play(self, simulation: Any, fps: float = 10.0) -> None:
        """Play a live simulation.

        The simulation is expected to expose either:
        - .world (world-like object) and .step() to advance, or
        - itself be world-like and expose .step().
        """

        delay = self._frame_delay(fps)
        paused = False
        want_step = False

        interactive = self._interactive_enabled()
        old_term_settings = None

        try:
            if interactive:
                old_term_settings = self._enter_cbreak_mode()

            sys.stdout.write(_HIDE_CURSOR)
            sys.stdout.flush()

            while True:
                world = getattr(simulation, "world", simulation)
                self._draw(world, fps=fps, paused=paused, interactive=interactive)

                cmd = self._read_key_nonblocking() if interactive else None
                if cmd == "q":
                    return
                if cmd == " ":
                    paused = not paused
                    want_step = False
                if cmd in ("s", "n"):
                    # Allow both 's' and 'n' for "step".
                    want_step = True

                if not paused or want_step:
                    self._advance_simulation(simulation)
                    want_step = False

                time.sleep(delay)

        except KeyboardInterrupt:
            return
        finally:
            if old_term_settings is not None:
                self._restore_terminal(old_term_settings)
            sys.stdout.write(_SHOW_CURSOR)
            sys.stdout.flush()

    def play_replay(self, reader: Any, fps: float = 10.0) -> None:
        """Play a replay from a ReplayReader-like object."""

        delay = self._frame_delay(fps)
        paused = False
        want_step = False

        interactive = self._interactive_enabled()
        old_term_settings = None

        try:
            if interactive:
                old_term_settings = self._enter_cbreak_mode()

            sys.stdout.write(_HIDE_CURSOR)
            sys.stdout.flush()

            start_tick, end_tick = getattr(reader, "tick_range")
            t = int(start_tick)
            while t <= int(end_tick):
                try:
                    frame = reader.get_frame(t)
                except KeyboardInterrupt:
                    return

                self._draw(frame, fps=fps, paused=paused, interactive=interactive)

                cmd = self._read_key_nonblocking() if interactive else None
                if cmd == "q":
                    return
                if cmd == " ":
                    paused = not paused
                    want_step = False
                if cmd in ("s", "n"):
                    want_step = True

                if not paused or want_step:
                    t += 1
                    want_step = False

                time.sleep(delay)

        except KeyboardInterrupt:
            return
        finally:
            if old_term_settings is not None:
                self._restore_terminal(old_term_settings)
            sys.stdout.write(_SHOW_CURSOR)
            sys.stdout.flush()

    def _draw(self, world: Any, *, fps: float, paused: bool, interactive: bool) -> None:
        grid = render_world_ascii(
            world,
            organism_char=self.organism_char,
            resource_char=self.resource_char,
            empty_char=self.empty_char,
        )
        tick = _world_tick(world)
        pop = _population(world)
        status = "paused" if paused else "playing"
        controls = "[space]=pause [s]=step [q]=quit" if interactive else "(non-interactive)"

        sys.stdout.write(_CLEAR)
        sys.stdout.write(grid)
        sys.stdout.write("\n")
        sys.stdout.write(
            f"tick={tick if tick is not None else '?'} pop={pop} fps={fps:g} {status} {controls}\n"
        )
        sys.stdout.flush()

    @staticmethod
    def _frame_delay(fps: float) -> float:
        f = float(fps)
        if f <= 0:
            # Treat non-positive as "as fast as reasonable" but non-busy.
            return 0.01
        return 1.0 / f

    @staticmethod
    def _advance_simulation(simulation: Any) -> None:
        step = getattr(simulation, "step", None)
        if callable(step):
            step()
            return
        world = getattr(simulation, "world", None)
        if world is not None:
            step2 = getattr(world, "step", None)
            if callable(step2):
                step2()

    @staticmethod
    def _interactive_enabled() -> bool:
        # If stdin isn't a TTY (e.g., tests, CI), we must not use termios.
        try:
            return bool(sys.stdin.isatty())
        except Exception:
            return False

    @staticmethod
    def _enter_cbreak_mode() -> Any:
        # Use termios/tty only when available and stdin is a TTY.
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        return old

    @staticmethod
    def _restore_terminal(old_settings: Any) -> None:
        import termios

        try:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
        except Exception:
            # Best-effort restore.
            pass

    @staticmethod
    def _read_key_nonblocking() -> Optional[str]:
        # Non-blocking single-char read.
        try:
            r, _, _ = select.select([sys.stdin], [], [], 0.0)
            if not r:
                return None
            ch = os.read(sys.stdin.fileno(), 1)
            if not ch:
                return None
            try:
                return ch.decode("utf-8", errors="ignore")
            except Exception:
                return None
        except Exception:
            return None
