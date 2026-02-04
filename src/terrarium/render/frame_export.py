from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from terrarium.render.ascii import AsciiRenderer


def export_ascii_frame(world: Any, path: str | Path) -> None:
    """Render *world* to ASCII and write it to *path* as UTF-8 text."""

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    renderer = AsciiRenderer()
    text = renderer.render(world)
    out_path.write_text(text, encoding="utf-8")


def export_ascii_frames(worlds: Iterable[Any], directory: str | Path) -> None:
    """Export multiple *worlds* as numbered ASCII frame files.

    Files are written as: frame_000001.txt, frame_000002.txt, ...
    """

    out_dir = Path(directory)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, world in enumerate(worlds, start=1):
        filename = f"frame_{i:06d}.txt"
        export_ascii_frame(world, out_dir / filename)
