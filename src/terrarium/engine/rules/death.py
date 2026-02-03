from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from terrarium.core.types import EntityId
from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


class _HasEnergy(Protocol):
    @property
    def id(self) -> EntityId: ...

    @property
    def energy(self) -> int: ...


@dataclass(frozen=True, slots=True)
class DeathRule:
    """Remove dead organisms from the world.

    Deterministic rule:
    - Any organism with energy <= 0 is removed.
    - Dead organisms are removed in the same tick they die.
    - Removal is done after collecting ids (no mutation during iteration).
    - Removal order is stable by entity id.

    Public API
    ----------
    apply(world) -> list[EntityId]
        Returns ids of removed organisms.
    """

    def apply(self, world: WorldState) -> list[EntityId]:
        # Collect first to avoid mutating while iterating.
        dead_ids: list[EntityId] = []

        for ent in list(world._entities.values()):  # type: ignore[attr-defined]
            # Phase 1 only targets Organism entities.
            if isinstance(ent, Organism):
                if int(ent.energy) <= 0:
                    dead_ids.append(ent.id)

        # Deterministic removal order.
        dead_ids = sorted(dead_ids, key=lambda eid: str(eid))

        for eid in dead_ids:
            world.remove_entity(eid)

        return dead_ids
