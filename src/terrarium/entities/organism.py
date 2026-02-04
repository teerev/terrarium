"""Organism entity.

An Organism represents a living agent in the world.

Scope notes:
- Organisms have mutable state (position, energy, age).
- Movement/reproduction/AI are out of scope for this work order.

Public APIs:
- :class:`Organism`
- :func:`create_organism`
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.base import EntityId, EntityType, generate_id
from terrarium.world.grid import Position


@dataclass(slots=True)
class Organism:
    """Living agent entity.

    Attributes:
        position: Current position (mutable).
        energy: Current energy (non-negative integer).
        age: Ticks since creation (starts at 0).
        id: Unique immutable entity id.
    """

    position: Position
    energy: int
    age: int = 0
    id: EntityId | None = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = generate_id()

        if not isinstance(self.energy, int) or self.energy < 0:
            raise ValueError("energy must be a non-negative integer")

        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("age must be a non-negative integer")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def is_alive(self) -> bool:
        return self.energy > 0

    def tick(self) -> int:
        """Advance organism internal time by one tick.

        Returns:
            The new age.
        """

        self.age += 1
        return self.age


def create_organism(position: Position, energy: int, *, entity_id: EntityId | None = None) -> Organism:
    """Factory for creating Organism instances with a valid id."""

    return Organism(position=position, energy=energy, id=entity_id)
