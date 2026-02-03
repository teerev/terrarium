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
from uuid import uuid4

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
    """Generate a new unique entity identifier."""

    return EntityId(uuid4().hex)


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
