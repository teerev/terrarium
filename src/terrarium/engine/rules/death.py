from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.base import EntityType
from terrarium.world.state import WorldState


@dataclass(slots=True)
class DeathRule:
    """Remove dead organisms from the world.

    Deterministic rule: any organism with energy <= 0 is removed.

    Public API
    ----------
    apply(world) -> list[EntityId]
        Returns IDs of removed organisms in deterministic order.
    """

    def apply(self, world: WorldState):
        dead_ids = []
        for e in world.iter_entities():
            if getattr(e, "entity_type", None) is not EntityType.ORGANISM:
                continue
            energy = getattr(e, "energy", None)
            if energy is None:
                continue
            if energy <= 0:
                dead_ids.append(getattr(e, "id"))

        # Deterministic removal order
        dead_ids.sort(key=lambda eid: str(eid))

        for eid in dead_ids:
            world.remove_entity(eid)

        return dead_ids
