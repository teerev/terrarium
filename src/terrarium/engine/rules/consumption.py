"""Resource consumption rule.

Organisms that occupy the same position as a resource will consume it, gaining
its energy value, and the resource will be removed from the world.

Determinism constraint:
- If multiple organisms are at the same position as a resource, process
  organisms in ID order; the first organism consumes the resource.

Public API:
- ConsumptionRule.apply(world, rng) -> list[ConsumptionEvent]

ConsumptionEvent is currently a placeholder for future eventing work orders.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from terrarium.entities.base import EntityType
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    """Placeholder event emitted when an organism consumes a resource."""

    organism_id: object
    resource_id: object
    energy_gained: int


class ConsumptionRule:
    """Rule that transfers energy from resources to organisms at the same position."""

    def apply(self, world: WorldState, rng: object) -> List[ConsumptionEvent]:
        # rng currently unused; kept for engine rule interface consistency.
        events: List[ConsumptionEvent] = []

        # Snapshot entities to avoid issues while removing resources.
        entities = list(world._entities.values())
        organisms = [e for e in entities if getattr(e, "entity_type", None) == EntityType.ORGANISM]

        # Deterministic processing order: by organism id.
        organisms.sort(key=lambda o: str(o.id))

        for org in organisms:
            # Organism might have been removed by other rules (not expected here,
            # but safe) or might have moved earlier in the tick.
            current = world.get_entity(org.id)
            if current is None or not isinstance(current, Organism):
                continue

            pos = current.position
            at_pos = world.get_entities_at(pos)
            resources = [e for e in at_pos if getattr(e, "entity_type", None) == EntityType.RESOURCE]
            if not resources:
                continue

            # Only one resource is consumed per organism per tick, and each
            # resource can only be consumed once because it is removed immediately.
            res = resources[0]
            if not isinstance(res, Resource):
                continue

            energy = res.consume()
            if energy <= 0:
                # Already consumed somehow; ensure it's removed to keep world consistent.
                world.remove_entity(res.id)
                continue

            current.energy += energy
            world.remove_entity(res.id)

            events.append(
                ConsumptionEvent(
                    organism_id=current.id,
                    resource_id=res.id,
                    energy_gained=energy,
                )
            )

        return events
