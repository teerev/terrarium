from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from terrarium.core.protocols import RandomSource
from terrarium.entities.base import EntityId, EntityType, generate_id
from terrarium.world.grid import Position


@dataclass(slots=True)
class Resource:
    """Stationary consumable energy source (food)."""

    position: Position
    energy_value: int
    id: EntityId
    consumed: bool = False

    def __post_init__(self) -> None:
        if self.energy_value <= 0:
            raise ValueError("energy_value must be a positive integer")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.RESOURCE


def create_resource(
    position: Position,
    energy_value: int,
    *,
    id: Optional[EntityId] = None,
    rng: Optional[RandomSource] = None,
) -> Resource:
    """Factory for Resource with a valid ID.

    If `rng` is provided and `id` is not, the id will be derived from the RNG for
    deterministic replay.
    """

    return Resource(position=position, energy_value=energy_value, id=id or generate_id(rng))
