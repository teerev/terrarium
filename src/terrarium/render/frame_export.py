from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from terrarium.render.ascii import AsciiRenderer, ColorScheme, render_world_ascii


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


def export_frame(
    world: Any,
    path: str | Path,
    *,
    color_by: str = "energy",
    color_scheme: ColorScheme | None = None,
) -> None:
    """Export a single frame.

    Public API (per work order):
    - export_frame(world, path, color_by='energy')

    Notes
    -----
    - This minimal implementation exports an ASCII frame.
    - Terminal ANSI color is intentionally disabled for file exports.
    """

    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    text = render_world_ascii(world, color=False, color_by=color_by, color_scheme=color_scheme)
    out_path.write_text(text, encoding="utf-8")
