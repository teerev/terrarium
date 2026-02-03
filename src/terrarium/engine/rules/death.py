from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from terrarium.core.types import EntityId
from terrarium.entities.organism import Organism
from terrarium.events.emitter import EventEmitter
from terrarium.events.schema import DeathCause, DeathEvent
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
    apply(world, emitter=None) -> list[EntityId]
        Returns ids of removed organisms.
    """

    def apply(self, world: WorldState, emitter: EventEmitter | None = None) -> list[EntityId]:
        # Collect first to avoid mutating while iterating.
        dead_ids: list[EntityId] = []
        dead_final_energy: dict[EntityId, int] = {}

        for ent in list(world._entities.values()):  # type: ignore[attr-defined]
            # Phase 1 only targets Organism entities.
            if isinstance(ent, Organism):
                if int(ent.energy) <= 0:
                    dead_ids.append(ent.id)
                    dead_final_energy[ent.id] = int(ent.energy)

        # Deterministic removal order.
        dead_ids = sorted(dead_ids, key=lambda eid: str(eid))

        for eid in dead_ids:
            if emitter is not None:
                emitter.emit(
                    DeathEvent(
                        tick=int(world.tick),
                        organism_id=eid,
                        cause=DeathCause.STARVATION,
                        final_energy=int(dead_final_energy.get(eid, 0)),
                    )
                )
            world.remove_entity(eid)

        return dead_ids
