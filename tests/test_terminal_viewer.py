from __future__ import annotations

from pathlib import Path

import pytest

from terrarium.cli import app
from terrarium.render.terminal import TerminalViewer


class _FakeReader:
    def __init__(self) -> None:
        self.tick_range = (0, 10)
        self._calls = 0

    def get_frame(self, tick: int) -> dict:
        self._calls += 1
        # Simulate user Ctrl+C occurring while fetching the next frame.
        if self._calls >= 2:
            raise KeyboardInterrupt
        return {
            "tick": int(tick),
            "grid": {"width": 2, "height": 2},
            "entities": [],
        }


def test_cli_watch_help_exits_zero(tmp_workdir: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # Ensure `watch --help` behaves like a normal help invocation and exits 0.
    code = app.main(["watch", "--help"], prog_name="terrarium", standalone_mode=False)
    assert code == 0
    out = capsys.readouterr().out
    assert "Watch a replay" in out


def test_terminal_viewer_play_replay_ctrl_c_exits_cleanly() -> None:
    # Must not raise.
    TerminalViewer().play_replay(_FakeReader(), fps=1000.0)
