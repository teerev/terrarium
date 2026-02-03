"""Organism entity.

Organisms represent living agents in the simulation.

Scope (P1.08)
------------
- Mutable state: position, energy, age
- Energy is non-negative
- Age increments each tick (via `tick()`)
- Satisfies the `Entity` protocol

Out of scope: movement logic, reproduction, genetics, behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from terrarium.world.grid import Position

from .base import Entity, EntityId, EntityType, generate_id


@dataclass(slots=True)
class Organism(Entity):
    """A living entity with mutable state."""

    # Keep `id` first and make other required fields keyword-only to avoid
    # dataclass ordering issues across Python versions.
    id: EntityId = field(default_factory=generate_id, kw_only=True)

    position: Position = field(kw_only=True)
    energy: int = 0
    age: int = 0

    def __post_init__(self) -> None:
        if self.energy < 0:
            raise ValueError("energy must be >= 0")
        if self.age < 0:
            raise ValueError("age must be >= 0")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def is_alive(self) -> bool:
        """Return True if this organism has positive energy."""

        return self.energy > 0

    def tick(self) -> int:
        """Advance organism internal age by one tick and return new age."""

        self.age += 1
        return self.age


def create_organism(
    position: Position, energy: int, *, id: EntityId | None = None
) -> Organism:
    """Factory for creating an Organism with a valid ID."""

    return Organism(
        position=position,
        energy=energy,
        age=0,
        id=generate_id() if id is None else id,
    )
