from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    """Event emitted when an organism consumes a resource."""

    tick: int
    organism_id: str
    resource_id: str
    energy_gained: int


class ConsumptionRule:
    """Rule: organisms consume resources located at their current position.

    - Deterministic: organisms are processed in id order.
    - A resource can only be consumed once per tick.
    - Full consumption transfers resource.energy_value to organism.energy.
    - Consumed resources are removed from the world immediately.
    """

    def apply(self, world: WorldState, rng: SeededRNG) -> list[ConsumptionEvent]:
        # rng is currently unused; included for API consistency with other rules.
        _ = rng

        events: list[ConsumptionEvent] = []

        # Snapshot lists so we can safely mutate world state during iteration.
        entities = list(world._entities.values())  # type: ignore[attr-defined]
        organisms = sorted(
            (e for e in entities if isinstance(e, Organism)),
            key=lambda o: str(o.id),
        )

        for org in organisms:
            # Always re-query resources at the organism's (wrapped) position.
            at_pos = world.get_entities_at(org.position)
            resources = [e for e in at_pos if isinstance(e, Resource) and not e.consumed]
            if not resources:
                continue

            # Consume exactly one resource at this position (no competition model beyond order).
            res = resources[0]
            gained = res.consume()
            if gained <= 0:
                # Already consumed by earlier processing.
                continue

            org.energy = org.energy + gained
            world.remove_entity(res.id)

            events.append(
                ConsumptionEvent(
                    tick=world.tick,
                    organism_id=str(org.id),
                    resource_id=str(res.id),
                    energy_gained=gained,
                )
            )

        return events
