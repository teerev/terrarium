from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import EntityId
from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(slots=True)
class DeathRule:
    """Remove organisms with non-positive energy from the world.

    Notes
    -----
    - Deterministic: energy <= 0 means death.
    - Applied after all energy updates for the tick.
    - Removals are collected first, then applied in deterministic order.
    """

    def apply(self, world: WorldState) -> list[EntityId]:
        dead: list[EntityId] = []

        # Collect first to avoid mutating while iterating.
        for e in world.iter_entities():
            if isinstance(e, Organism) and e.energy <= 0:
                dead.append(e.id)

        # Deterministic removal order by string form.
        dead_sorted = sorted(dead, key=lambda eid: str(eid))
        for eid in dead_sorted:
            world.remove_entity(eid)

        return dead_sorted
