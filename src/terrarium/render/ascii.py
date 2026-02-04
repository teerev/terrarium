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

    # World Position is a dataclass with x/y
    if hasattr(pos, "x") and hasattr(pos, "y"):
        try:
            return (int(getattr(pos, "x")), int(getattr(pos, "y")))
        except Exception:
            pass

    # Snapshot dicts store [x,y]
    if isinstance(entity, Mapping):
        p2 = entity.get("position")
        if isinstance(p2, (list, tuple)) and len(p2) == 2:
            return (int(p2[0]), int(p2[1]))

    return None


def _entity_energy(entity: Any) -> int | None:
    val = getattr(entity, "energy", None)
    if val is None and isinstance(entity, Mapping):
        val = entity.get("energy")
    if val is None:
        return None
    try:
        return int(val)
    except Exception:
        return None


def _entity_age(entity: Any) -> int | None:
    val = getattr(entity, "age", None)
    if val is None and isinstance(entity, Mapping):
        val = entity.get("age")
    if val is None:
        return None
    try:
        return int(val)
    except Exception:
        return None


def _entity_species_key(entity: Any) -> str:
    # Prefer an explicit species_id if present; else fall back to lineage_id; else id.
    for attr in ("species_id", "species", "lineage_id", "id"):
        v = getattr(entity, attr, None)
        if v is not None:
            return str(v)
        if isinstance(entity, Mapping) and attr in entity:
            try:
                return str(entity.get(attr))
            except Exception:
                pass
    return ""


@dataclass(frozen=True, slots=True)
class ColorScheme:
    """Minimal, configurable color scheme for terminal ANSI output."""

    # Energy thresholds are expressed as fractions of max_energy.
    energy_low_threshold: float = 0.25
    energy_mid_threshold: float = 0.5

    # Terminal colors (ANSI SGR sequences)
    reset: str = "\033[0m"
    energy_low: str = "\033[31m"  # red
    energy_mid: str = "\033[33m"  # yellow
    energy_high: str = "\033[32m"  # green

    # Species colors should be distinguishable; keep a small cycle.
    species_cycle: tuple[str, ...] = (
        "\033[36m",  # cyan
        "\033[35m",  # magenta
        "\033[34m",  # blue
        "\033[32m",  # green
        "\033[33m",  # yellow
        "\033[31m",  # red
    )

    # Age colors: younger brighter, older dimmer (approximation)
    age_young: str = "\033[1m"  # bold
    age_old: str = "\033[2m"  # dim


def _ansi_wrap(text: str, *, prefix: str, reset: str) -> str:
    return f"{prefix}{text}{reset}"


def _pick_species_color(scheme: ColorScheme, species_key: str) -> str:
    if not scheme.species_cycle:
        return scheme.reset
    idx = abs(hash(species_key)) % len(scheme.species_cycle)
    return scheme.species_cycle[idx]


def _pick_energy_color(scheme: ColorScheme, energy: int, max_energy: int) -> str:
    if max_energy <= 0:
        return scheme.energy_high
    frac = energy / max_energy
    if frac < scheme.energy_low_threshold:
        return scheme.energy_low
    if frac < scheme.energy_mid_threshold:
        return scheme.energy_mid
    return scheme.energy_high


def _pick_age_color(scheme: ColorScheme, age: int, max_age: int) -> str:
    if max_age <= 0:
        return scheme.age_young
    frac = age / max_age
    # young (lower frac): bold; old: dim
    return scheme.age_old if frac >= 0.5 else scheme.age_young


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
    color: bool = False,
    color_by: str = "energy",
    color_scheme: ColorScheme | None = None,
    max_energy: int | None = None,
    max_age: int | None = None,
) -> str:
    """Render *world* as a simple ASCII grid.

    Public API:
    - terrarium.render.render_world_ascii(world, color=False, color_by='energy') -> str

    Notes
    -----
    - Organisms override resources when multiple entities occupy the same cell.
    - Supports WorldState objects and snapshot/replay dicts (with keys: grid, entities).
    - If *color* is False, output contains no ANSI escape codes.
    """

    scheme = color_scheme if color_scheme is not None else ColorScheme()

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

    ents = list(_iter_entities(world))

    # Derive maxima if not provided.
    if max_energy is None:
        energies = [e for e in (_entity_energy(ent) for ent in ents) if e is not None]
        max_energy = max(energies) if energies else 1
    if max_age is None:
        ages = [a for a in (_entity_age(ent) for ent in ents) if a is not None]
        max_age = max(ages) if ages else 1

    # Base raster
    grid_chars: list[list[str]] = [[empty_char for _ in range(width)] for _ in range(height)]

    # Place resources first, then organisms.
    for pass_type, ch in (("resource", resource_char), ("organism", organism_char)):
        for e in ents:
            et = _entity_type(e)
            if et != pass_type:
                continue
            pos = _entity_pos(e)
            if pos is None:
                continue
            x, y = pos
            if not (0 <= x < width and 0 <= y < height):
                continue

            if not color or pass_type != "organism":
                grid_chars[y][x] = ch
                continue

            mode = str(color_by or "energy")
            if mode == "species":
                c = _pick_species_color(scheme, _entity_species_key(e))
            elif mode == "age":
                age = _entity_age(e) or 0
                c = _pick_age_color(scheme, age, int(max_age))
            else:  # energy (default)
                energy = _entity_energy(e) or 0
                c = _pick_energy_color(scheme, energy, int(max_energy))

            grid_chars[y][x] = _ansi_wrap(ch, prefix=c, reset=scheme.reset)

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
