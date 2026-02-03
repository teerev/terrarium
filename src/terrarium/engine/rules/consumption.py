"""Resource consumption rule.

Scope (P1.11)
------------
- Organisms at the same position as a resource can consume it.
- Consuming transfers the resource's full energy_value to the organism.
- Consumed resources are removed from the world immediately.
- Deterministic: when multiple organisms are on the same resource, the first
  organism processed (by deterministic ID order) consumes it.

Out of scope
------------
- Partial consumption
- Competition beyond first-come (by ordering)
- Cooldowns / digestion modifiers

Public API
----------
- ConsumptionRule.apply(world, rng) -> list[ConsumptionEvent]

Notes
-----
The rule does not currently use rng, but accepts it for future extensibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from terrarium.core.protocols import RandomSource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


class _HasEnergyAndPosition(Protocol):
    id: object
    position: Position
    energy: int


class _ResourceLike(Protocol):
    id: object
    position: Position
    energy_value: int
    consumed: bool

    def consume(self) -> int: ...


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    """Structured record of a consumption interaction."""

    organism_id: object
    resource_id: object
    position: Position
    energy_gained: int


@dataclass(frozen=True, slots=True)
class ConsumptionRule:
    """Allow organisms to consume resources at their current position."""

    def apply(self, world: WorldState, rng: RandomSource) -> list[ConsumptionEvent]:
        _ = rng  # reserved for future use

        organisms: list[_HasEnergyAndPosition] = []
        resources: list[_ResourceLike] = []

        for e in world.iter_entities():
            et = getattr(e, "entity_type", None)
            if getattr(et, "value", et) == "organism":
                organisms.append(e)  # type: ignore[arg-type]
            elif getattr(et, "value", et) == "resource":
                resources.append(e)  # type: ignore[arg-type]

        if not organisms or not resources:
            return []

        # Deterministic organism processing order (matches other phases).
        organisms.sort(key=lambda o: str(getattr(o, "id")))

        # Build a stable lookup for resources by position.
        resources_by_pos: dict[Position, list[_ResourceLike]] = {}
        for r in resources:
            pos = world.grid.wrap(r.position)
            resources_by_pos.setdefault(pos, []).append(r)

        # Stable resource selection within a cell if multiple resources exist.
        for pos, rs in resources_by_pos.items():
            rs.sort(key=lambda r: str(getattr(r, "id")))

        events: list[ConsumptionEvent] = []
        for o in organisms:
            pos = world.grid.wrap(o.position)
            rs = resources_by_pos.get(pos)
            if not rs:
                continue

            # Consume at most one resource per organism per tick.
            r = rs.pop(0)
            if not rs:
                resources_by_pos.pop(pos, None)

            gained = int(r.consume())
            o.energy = int(o.energy) + gained
            world.remove_entity(r.id)

            events.append(
                ConsumptionEvent(
                    organism_id=o.id,
                    resource_id=r.id,
                    position=pos,
                    energy_gained=gained,
                )
            )

        return events
