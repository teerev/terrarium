"""Testing helpers for terrarium.

This module is intentionally small and stable. It provides utilities that tests
(and optionally downstream users) can use to compare simulation results.
"""

from __future__ import annotations

from typing import Any

from terrarium.entities.base import EntityType
from terrarium.world.state import WorldState


def snapshot_world_state(world: WorldState) -> dict[str, Any]:
    """Create a deterministic, JSON-serializable snapshot of a world.

    Snapshot includes:
    - grid dimensions
    - seed
    - tick
    - entities (id, type, position, and key attributes)

    Entity ordering is stable (sorted by stringified id).
    """

    entities: list[dict[str, Any]] = []
    for e in world.iter_entities():
        et = getattr(e, "entity_type", None)
        if isinstance(et, EntityType):
            et_val = et.value
        else:
            et_val = getattr(et, "value", et)

        d: dict[str, Any] = {
            "id": str(getattr(e, "id")),
            "type": str(et_val),
            "x": int(getattr(getattr(e, "position"), "x")),
            "y": int(getattr(getattr(e, "position"), "y")),
        }

        if et_val == EntityType.ORGANISM.value or et_val == "organism":
            d["energy"] = int(getattr(e, "energy"))
            d["age"] = int(getattr(e, "age"))
        elif et_val == EntityType.RESOURCE.value or et_val == "resource":
            d["energy_value"] = int(getattr(e, "energy_value"))
            d["consumed"] = bool(getattr(e, "consumed"))

        entities.append(d)

    entities.sort(key=lambda x: x["id"])

    return {
        "grid": {"width": int(world.grid.width), "height": int(world.grid.height)},
        "seed": int(world.seed),
        "tick": int(world.tick),
        "entities": entities,
    }
