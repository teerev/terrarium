from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class DeathRule:
    """Rule for removing dead organisms from the world.

    Design constraints:
    - Deterministic: organisms with energy <= 0 are removed
    - Deaths processed in the same tick they occur
    - Removal updates all WorldState indices via WorldState.remove_entity

    Public API:
    - DeathRule.apply(world) -> list[EntityId]
    """

    def apply(self, world: WorldState) -> list[object]:
        # WorldState doesn't expose an organism iterator; keep changes localized
        # by iterating the internal index.
        entities = getattr(world, "_entities", {})

        dead: list[tuple[str, object]] = []
        for e in entities.values():
            if isinstance(e, Organism) and e.energy <= 0:
                dead.append((str(e.id), e.id))

        # Deterministic removal order.
        dead.sort(key=lambda t: t[0])

        removed: list[object] = []
        for _sid, eid in dead:
            world.remove_entity(eid)
            removed.append(eid)

        return removed
