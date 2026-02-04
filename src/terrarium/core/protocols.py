"""Protocol (interface) definitions for simulation components.

These Protocols define the minimal behaviors expected of worlds, entities, and
random sources without committing to concrete implementations.
"""

from __future__ import annotations

from typing import Protocol

from .types import EntityId, Position


class RandomSource(Protocol):
    """Abstract random source used by the engine.

    The engine should depend on this interface instead of a concrete RNG to
    allow deterministic tests and alternative RNG implementations.
    """

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""


class Entity(Protocol):
    """An object that can exist in a world.

    Concrete entity implementations typically live in :mod:`terrarium.entities`.
    """

    @property
    def id(self) -> EntityId:
        """Unique identifier for this entity within its world."""

    @property
    def position(self) -> Position:
        """Current position of the entity in the world."""


class World(Protocol):
    """A container for world state.

    Concrete world implementations typically live in :mod:`terrarium.world`.
    """

    def get_entity(self, entity_id: EntityId) -> Entity | None:
        """Look up an entity by id."""
