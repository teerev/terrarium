from __future__ import annotations

from terrarium.entities.base import EntityId, EntityType, generate_id
from terrarium.world.grid import Position


class Organism:
    """A living, mutable agent.

    Organisms have mutable state: position, energy, and age.
    """

    def __init__(
        self,
        position: Position,
        energy: int,
        *,
        id: EntityId | None = None,
    ) -> None:
        self._id: EntityId = generate_id() if id is None else id
        self._position: Position = position
        self._energy: int = int(energy)
        if self._energy < 0:
            raise ValueError("energy must be a non-negative integer")
        self._age: int = 0

    @property
    def id(self) -> EntityId:
        return self._id

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        v = int(value)
        if v < 0:
            raise ValueError("energy must be a non-negative integer")
        self._energy = v

    @property
    def age(self) -> int:
        return self._age

    @property
    def is_alive(self) -> bool:
        return self._energy > 0

    def tick(self) -> int:
        """Advance organism age by one tick and return new age."""

        self._age += 1
        return self._age


def create_organism(
    position: Position,
    energy: int,
    *,
    id: EntityId | None = None,
) -> Organism:
    """Factory for Organism with generated id if not provided."""

    return Organism(position=position, energy=energy, id=id)
