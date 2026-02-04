"""Resource entity.

A Resource represents a stationary, consumable energy source in the world.
"""

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
        if self.id is None:
            self.id = generate_id()
        if not isinstance(self.energy_value, int) or self.energy_value <= 0:
            raise ValueError("energy_value must be a positive integer")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.RESOURCE

    def consume(self) -> int:
        """Mark as consumed and return the energy provided.

        Note: removal from the world is handled by WorldState.remove_entity.
        """

        if self.consumed:
            return 0
        self.consumed = True
        return self.energy_value


def create_resource(
    position: Position,
    energy_value: int,
    *,
    entity_id: EntityId | None = None,
    rng: SeededRNG | None = None,
) -> Resource:
    """Factory for creating Resource instances with a valid id.

    Determinism:
    - If entity_id is provided, it is used as-is.
    - Else if rng is provided, a deterministic id is generated from it.
    - Else a non-deterministic uuid4 id is generated.
    """

    if entity_id is None and rng is not None:
        entity_id = generate_id_from_rng(rng)

    return Resource(position=position, energy_value=energy_value, id=entity_id)
