from __future__ import annotations

"""Entity base protocol.

This module defines the minimal interface (protocol) that all simulation
entities must implement.

Contract:
- Entity IDs are unique and immutable once assigned.
- Position is gettable and settable.
- Entity type is identifiable for filtering/categorization.

The protocol is intended for structural subtyping (mypy-friendly): any object
with matching attributes satisfies the protocol without inheriting from a base
class.
"""

from enum import Enum
from typing import NewType, Protocol

from terrarium.engine.rng import SeededRNG
from terrarium.world.grid import Position


EntityId = NewType("EntityId", str)
"""A stable identifier for an entity within a simulation.

Represented as a string for easy serialization/logging. IDs should be treated
as immutable once assigned to an entity.
"""


class EntityType(str, Enum):
    """High-level category for entities."""

    ORGANISM = "organism"
    RESOURCE = "resource"


def generate_id() -> EntityId:
    """Generate a new unique entity identifier.

    Note
    ----
    This function is kept for backward compatibility. For deterministic
    simulations, prefer :func:`generate_id_from_rng`.
    """

    # Default path remains non-deterministic, but tests and simulation should
    # use generate_id_from_rng (or pass explicit ids).
    import uuid

    return EntityId(uuid.uuid4().hex)


def generate_id_from_rng(rng: SeededRNG) -> EntityId:
    """Generate a deterministic entity id using the provided seeded RNG."""

    # Use full 128-bit space for UUID-like ids.
    n = rng.randint(0, 2**128 - 1)
    return EntityId(f"{n:032x}")


class Entity(Protocol):
    """Base protocol implemented by all simulation entities."""

    @property
    def id(self) -> EntityId:
        """Stable, unique entity identifier."""

    @property
    def position(self) -> Position:
        """Current position in the world."""

    @position.setter
    def position(self, value: Position) -> None:
        """Update the current position in the world."""

    @property
    def entity_type(self) -> EntityType:
        """Entity category used for filtering/categorization."""
