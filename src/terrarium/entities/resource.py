"""Resource entity.

Resources represent stationary consumable energy sources (food) in the world.

Design constraints
------------------
- Stationary: position does not change after creation.
- Fixed energy value: positive integer set at creation.
- Removable: can be marked consumed and removed from the world.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from terrarium.core.protocols import RandomSource
from terrarium.world.grid import Position

from .base import Entity, EntityId, EntityType, generate_id


@dataclass(slots=True)
class Resource(Entity):
    """A stationary consumable energy source."""

    # Python 3.12 dataclasses enforce that fields without defaults cannot follow
    # fields with defaults (even if kw_only). Keep `id` first and make the
    # remaining required fields keyword-only to avoid ordering issues.
    id: EntityId = field(default_factory=generate_id, kw_only=True)

    position: Position = field(kw_only=True)
    energy_value: int = field(kw_only=True)
    consumed: bool = False

    def __post_init__(self) -> None:
        if self.energy_value <= 0:
            raise ValueError("energy_value must be a positive integer")

    @property
    def entity_type(self) -> EntityType:
        return EntityType.RESOURCE

    def consume(self) -> int:
        """Mark as consumed and return the energy value.

        This method does not remove the resource from the world; callers should
        remove it from WorldState when appropriate.

        Raises
        ------
        RuntimeError
            If the resource has already been consumed.
        """

        if self.consumed:
            raise RuntimeError("Resource already consumed")
        self.consumed = True
        return int(self.energy_value)


def create_resource(
    position: Position,
    energy_value: int,
    *,
    id: EntityId | None = None,
    rng: RandomSource | None = None,
) -> Resource:
    """Factory for creating a Resource with a valid ID.

    If *id* is provided, it is used directly.
    Else if *rng* is provided, the ID is generated deterministically from it.
    Else a non-deterministic ID is generated.
    """

    return Resource(
        position=position,
        energy_value=energy_value,
        id=generate_id(rng) if id is None else id,
    )
