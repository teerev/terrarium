from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.base import EntityId, EntityType, generate_id, generate_id_from_rng
from terrarium.world.grid import Position


@dataclass(slots=True)
class Resource:
    """Stationary consumable energy source."""

    position: Position
    energy_value: int
    id: EntityId | None = None
    consumed: bool = False

    def __post_init__(self) -> None:
        if int(self.energy_value) <= 0:
            raise ValueError("energy_value must be a positive integer")
        self.energy_value = int(self.energy_value)
        if self.id is None:
            self.id = generate_id()

    @property
    def entity_type(self) -> EntityType:
        return EntityType.RESOURCE

    def consume(self) -> int:
        """Mark resource as consumed and return its energy value.

        Consumption is idempotent.
        """

        if self.consumed:
            return 0
        self.consumed = True
        return self.energy_value


def create_resource(
    position: Position,
    energy_value: int,
    *,
    id: EntityId | None = None,
    rng: SeededRNG | None = None,
) -> Resource:
    """Factory for Resource with deterministic id generation when rng is provided."""

    if id is None:
        if rng is not None:
            id = generate_id_from_rng(rng)

    return Resource(position=position, energy_value=energy_value, id=id)
