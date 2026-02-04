from __future__ import annotations

from terrarium.render.frame_export import export_ascii_frame, export_ascii_frames
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_export_ascii_frame_writes_file(tmp_workdir):
    world = WorldState(Grid(3, 2), seed=1)
    out_path = tmp_workdir / "frame.txt"

    export_ascii_frame(world, out_path)

    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    assert "+---+" in text
    assert "size=3x2" in text


def test_export_ascii_frames_creates_numbered_files(tmp_workdir):
    worlds = [WorldState(Grid(2, 2), seed=1), WorldState(Grid(2, 2), seed=2)]
    out_dir = tmp_workdir / "frames"

    export_ascii_frames(worlds, out_dir)

    f1 = out_dir / "frame_000001.txt"
    f2 = out_dir / "frame_000002.txt"
    assert f1.exists()
    assert f2.exists()
