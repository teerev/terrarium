from __future__ import annotations

from typing import Any

from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


def snapshot_world_state(world: WorldState) -> dict[str, Any]:
    """Return a deterministic, deep-ish snapshot of the world's state.

    Snapshot is designed for test comparisons and includes:
    - tick
    - grid dimensions
    - entity list with stable ordering and key state for known entity types
    """

    entities = list(world._entities.values())  # type: ignore[attr-defined]

    def ent_key(e: Any) -> str:
        return str(getattr(e, "id", ""))

    items: list[dict[str, Any]] = []
    for ent in sorted(entities, key=ent_key):
        base: dict[str, Any] = {
            "id": str(getattr(ent, "id")),
            "type": str(getattr(ent, "entity_type", type(ent).__name__)),
            "position": (
                int(getattr(getattr(ent, "position"), "x")),
                int(getattr(getattr(ent, "position"), "y")),
            ),
        }

        if isinstance(ent, Organism):
            base.update({"energy": int(ent.energy), "age": int(ent.age)})
        elif isinstance(ent, Resource):
            base.update({"energy_value": int(ent.energy_value), "consumed": bool(ent.consumed)})

        items.append(base)

    return {
        "tick": int(world.tick),
        "grid": {"width": int(world.grid.width), "height": int(world.grid.height)},
        "entities": items,
    }
