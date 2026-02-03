"""Base entity protocol and identifiers.

This module defines the minimal interface (contract) that all simulation entities
must satisfy. Entities are intentionally modeled via ``typing.Protocol`` for
structural subtyping to avoid inheritance-heavy designs.

Contract
--------
An entity must provide:
- ``id``: an immutable unique identifier (EntityId)
- ``position``: gettable and settable spatial position
- ``entity_type``: a coarse category for filtering/grouping

The protocol is designed to be compatible with mypy structural typing.
"""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable
from uuid import UUID, uuid4

from terrarium.world.grid import Position

EntityId = UUID
"""Immutable unique identifier for an entity.

We use UUIDs to ensure uniqueness without coordination or global state.
"""


class EntityType(str, Enum):
    """Coarse entity categories.

    This enables filtering/grouping without relying on concrete classes.
    """

    ORGANISM = "organism"
    RESOURCE = "resource"


def generate_id() -> EntityId:
    """Generate a new unique entity id."""

    return uuid4()


@runtime_checkable
class Entity(Protocol):
    """Base protocol that all simulation entities must implement."""

    @property
    def id(self) -> EntityId:
        """Immutable unique entity identifier."""

    @property
    def position(self) -> Position:
        """Current entity position."""

    @position.setter
    def position(self, value: Position) -> None:
        """Update entity position."""

    @property
    def entity_type(self) -> EntityType:
        """Entity category."""
