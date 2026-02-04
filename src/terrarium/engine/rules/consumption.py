from __future__ import annotations

from dataclasses import dataclass
from typing import List

from terrarium.core.protocols import RandomSource
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    """Event emitted when an organism consumes a resource."""

    organism_id: object
    resource_id: object
    energy_gained: int


class ConsumptionRule:
    """Allow organisms to consume resources occupying the same grid position.

    Determinism:
    - For each resource, organisms at that position are processed by organism id order.
    - The first organism consumes the resource.

    Scope notes:
    - No partial consumption.
    - No competition resolution beyond deterministic ordering.
    """

    def apply(self, world: WorldState, rng: RandomSource) -> List[ConsumptionEvent]:
        # rng currently unused; kept for API compatibility and future extensions.
        del rng

        events: List[ConsumptionEvent] = []

        organisms: list[Organism] = []
        resources: list[Resource] = []
        for e in world.iter_entities():
            if isinstance(e, Organism):
                organisms.append(e)
            elif isinstance(e, Resource):
                resources.append(e)

        organisms_by_pos: dict[object, list[Organism]] = {}
        for org in organisms:
            pos = world.grid.wrap(org.position)
            organisms_by_pos.setdefault(pos, []).append(org)

        for pos, orgs in organisms_by_pos.items():
            orgs.sort(key=lambda o: str(o.id))

        # Process resources in deterministic order too (helps repeatability)
        resources.sort(key=lambda r: str(r.id))

        for res in resources:
            if res.consumed:
                continue

            pos = world.grid.wrap(res.position)
            candidates = organisms_by_pos.get(pos)
            if not candidates:
                continue

            consumer = candidates[0]
            consumer.energy += res.energy_value
            res.consumed = True
            world.remove_entity(res.id)

            events.append(
                ConsumptionEvent(
                    organism_id=consumer.id,
                    resource_id=res.id,
                    energy_gained=res.energy_value,
                )
            )

        return events
