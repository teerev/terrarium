from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from terrarium.world.state import WorldState


def _get_grid_size(world: Any) -> tuple[int, int]:
    grid = getattr(world, "grid", None)
    if grid is None:
        raise TypeError("world must have a .grid with width/height")
    width = int(getattr(grid, "width"))
    height = int(getattr(grid, "height"))
    return width, height


def _iter_entities(world: Any) -> Iterable[Any]:
    # Prefer WorldState internals for efficiency, fall back to snapshot-like dict.
    if isinstance(world, WorldState):
        return list(world._entities.values())  # type: ignore[attr-defined]

    if isinstance(world, Mapping):
        ents = world.get("entities")
        if isinstance(ents, list):
            return ents
        return []

    # Unknown world type: try a generic attribute.
    ents2 = getattr(world, "entities", None)
    if isinstance(ents2, list):
        return ents2
    return []


def _entity_type(entity: Any) -> str:
    # World objects: entity.entity_type is an Enum (EntityType)
    et = getattr(entity, "entity_type", None)
    if et is not None:
        return str(getattr(et, "value", et))

    # Snapshot dicts use "type"
    if isinstance(entity, Mapping):
        t = entity.get("type")
        if t is not None:
            return str(t)

    return ""


def _entity_pos(entity: Any) -> tuple[int, int] | None:
    pos = getattr(entity, "position", None)

    # World Position is a tuple[int,int]
    if isinstance(pos, tuple) and len(pos) == 2:
        return (int(pos[0]), int(pos[1]))

    # Snapshot dicts store [x,y]
    if isinstance(entity, Mapping):
        p2 = entity.get("position")
        if isinstance(p2, (list, tuple)) and len(p2) == 2:
            return (int(p2[0]), int(p2[1]))

    return None


@dataclass(frozen=True, slots=True)
class AsciiRenderer:
    organism_char: str = "O"
    resource_char: str = "*"
    empty_char: str = "."

    def render(self, world: Any) -> str:
        return render_world_ascii(
            world,
            organism_char=self.organism_char,
            resource_char=self.resource_char,
            empty_char=self.empty_char,
        )


def render_world_ascii(
    world: Any,
    *,
    organism_char: str = "O",
    resource_char: str = "*",
    empty_char: str = ".",
) -> str:
    """Render *world* as a simple ASCII grid.

    Public API:
    - terrarium.render.render_world_ascii(world) -> str

    Notes
    -----
    - Organisms override resources when multiple entities occupy the same cell.
    - Supports WorldState objects and snapshot/replay dicts (with keys: grid, entities).
    """

    # Support replay/snapshot dicts that carry grid dims under world["grid"].
    if isinstance(world, Mapping) and "grid" in world:
        g = world.get("grid")
        if isinstance(g, Mapping):
            width = int(g.get("width", 0))
            height = int(g.get("height", 0))
        else:
            width, height = _get_grid_size(world)
    else:
        width, height = _get_grid_size(world)

    if width <= 0 or height <= 0:
        raise ValueError("world grid must have positive width/height")

    # Base raster
    grid_chars: list[list[str]] = [[empty_char for _ in range(width)] for _ in range(height)]

    # Place resources first, then organisms.
    for pass_type, ch in (("resource", resource_char), ("organism", organism_char)):
        for e in _iter_entities(world):
            et = _entity_type(e)
            if et != pass_type:
                continue
            pos = _entity_pos(e)
            if pos is None:
                continue
            x, y = pos
            if 0 <= x < width and 0 <= y < height:
                grid_chars[y][x] = ch

    top = "+" + ("-" * width) + "+"
    lines = [top]
    for y in range(height):
        lines.append("|" + "".join(grid_chars[y]) + "|")
    lines.append(top)

    tick = getattr(world, "tick", None)
    if isinstance(world, Mapping):
        tick = world.get("tick", tick)
    if tick is not None:
        try:
            lines.append(f"tick={int(tick)} size={width}x{height}")
        except Exception:
            lines.append(f"size={width}x{height}")
    else:
        lines.append(f"size={width}x{height}")

    return "\n".join(lines)
