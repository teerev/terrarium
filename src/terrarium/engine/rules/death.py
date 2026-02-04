from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.organism import Organism
from terrarium.events.emitter import EventEmitter
from terrarium.events.schema import DeathCause, DeathEvent
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class DeathRule:
    """Rule for removing dead organisms from the world.

    Design constraints:
    - Deterministic: organisms with energy <= 0 are removed
    - Deaths processed in the same tick they occur
    - Removal updates all WorldState indices via WorldState.remove_entity

    Public API:
    - DeathRule.apply(world, emitter=None) -> list[EntityId]
    """

    def apply(self, world: WorldState, emitter: EventEmitter | None = None) -> list[object]:
        # WorldState doesn't expose an organism iterator; keep changes localized
        # by iterating the internal index.
        entities = getattr(world, "_entities", {})

        dead: list[tuple[str, Organism]] = []
        for e in entities.values():
            if isinstance(e, Organism) and e.energy <= 0:
                dead.append((str(e.id), e))

        # Deterministic removal order.
        dead.sort(key=lambda t: t[0])

        removed: list[object] = []
        for _sid, org in dead:
            # Emit death event before organism removed.
            if emitter is not None:
                emitter.emit(
                    DeathEvent(
                        tick=world.tick,
                        organism_id=org.id,  # type: ignore[arg-type]
                        cause=DeathCause.STARVATION.value,
                        final_energy=int(org.energy),
                    )
                )

            world.remove_entity(org.id)
            removed.append(org.id)

        return removed
