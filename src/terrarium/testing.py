"""Testing helpers for Terrarium.

Public API:
- snapshot_world_state(world) -> dict

The returned dict is JSON-serializable (assuming entity ids stringify) and is
stable under entity ordering differences.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


def _xy(pos: object) -> tuple[int, int]:
    """Extract (x, y) from either a dataclass Position(x,y) or a tuple (x,y)."""

    # terrarium.world.grid.Position is a dataclass with x/y
    x = getattr(pos, "x", None)
    y = getattr(pos, "y", None)
    if x is not None and y is not None:
        return int(x), int(y)

    # terrarium.core.types.Position is a Tuple[int, int]
    if isinstance(pos, tuple) and len(pos) == 2:
        return int(pos[0]), int(pos[1])

    raise TypeError(f"Unsupported position type: {type(pos)!r}")


def snapshot_world_state(world: WorldState) -> Dict[str, Any]:
    """Create a deterministic snapshot of world state for comparisons."""

    entities = list(getattr(world, "_entities", {}).values())

    organisms: List[Tuple[str, int, int, int]] = []
    resources: List[Tuple[str, int, int, int, bool]] = []

    for e in entities:
        if isinstance(e, Organism):
            x, y = _xy(e.position)
            organisms.append((str(e.id), x, y, int(e.energy)))
        elif isinstance(e, Resource):
            x, y = _xy(e.position)
            resources.append((str(e.id), x, y, int(e.energy_value), bool(e.consumed)))

    organisms.sort(key=lambda t: t[0])
    resources.sort(key=lambda t: t[0])

    return {
        "tick": int(world.tick),
        "grid": {"width": int(world.grid.width), "height": int(world.grid.height)},
        "organisms": [
            {"id": oid, "x": x, "y": y, "energy": energy} for (oid, x, y, energy) in organisms
        ],
        "resources": [
            {"id": rid, "x": x, "y": y, "energy_value": ev, "consumed": consumed}
            for (rid, x, y, ev, consumed) in resources
        ],
    }
