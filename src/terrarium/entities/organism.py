from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from terrarium.core.protocols import RandomSource
from terrarium.entities.base import EntityId, EntityType, generate_id
from terrarium.world.grid import Position


@dataclass(slots=True)
class Organism:
    """Living entity with mutable state.

    Notes:
    - position is mutable so the engine/world can move organisms.
    - energy is mutable and must be non-negative.
    - age starts at 0 and can be incremented externally each tick.
    """

    position: Position
    energy: int
    id: EntityId
    age: int = 0

    def __post_init__(self) -> None:
        if self.energy < 0:
            raise ValueError("energy must be non-negative")
        if self.age < 0:
            raise ValueError("age must be non-negative")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.ORGANISM

    @property
    def is_alive(self) -> bool:
        return self.energy > 0


def create_organism(
    position: Position,
    energy: int,
    *,
    id: Optional[EntityId] = None,
    rng: Optional[RandomSource] = None,
) -> Organism:
    """Factory for Organism with a valid ID.

    If `rng` is provided and `id` is not, the id will be derived from the RNG for
    deterministic replay.
    """

    return Organism(position=position, energy=energy, id=id or generate_id(rng))
