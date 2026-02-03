from __future__ import annotations


def test_export_replay_importable() -> None:
    from terrarium.io.replay import ReplayFormat, export_replay

    assert ReplayFormat().version >= 1
    assert callable(export_replay)
