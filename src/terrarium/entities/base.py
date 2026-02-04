"""Base entity protocol and shared entity utilities.

This module defines the minimal *structural* interface (via ``typing.Protocol``)
that all simulation entities must implement.

Public APIs:
- :class:`Entity` protocol
- :data:`EntityId` type alias
- :class:`EntityType` enum
- :func:`generate_id` unique ID generator

Design notes:
- Entity IDs are intended to be unique and immutable once assigned.
- ``position`` must be gettable and settable to allow movement.
- ``entity_type`` allows filtering/grouping entities by category.

Determinism constraint:
- IDs must be generated deterministically when running seeded simulations.
  Callers may supply an explicit id or use :func:`generate_id_from_rng`.
"""

from __future__ import annotations

from enum import Enum
from typing import NewType, Protocol
import uuid

from terrarium.engine.rng import SeededRNG
from terrarium.world.grid import Position


EntityId = NewType("EntityId", uuid.UUID)
"""Identifier for an entity.

Implemented as a :class:`uuid.UUID` wrapped in :func:`typing.NewType` to keep
runtime cost low while providing stronger type-checking.

IDs should be treated as immutable.
"""


class EntityType(str, Enum):
    """High-level categories for entities."""

    ORGANISM = "organism"
    RESOURCE = "resource"


def generate_id() -> EntityId:
    """Generate a fresh unique entity id.

    Note
    ----
    This uses :func:`uuid.uuid4` and is therefore *not deterministic*. Seeded
    simulations should instead use :func:`generate_id_from_rng`.
    """

    return EntityId(uuid.uuid4())


def generate_id_from_rng(rng: SeededRNG) -> EntityId:
    """Generate a deterministic UUID derived from the provided seeded RNG."""

    # Use a deterministic 128-bit int from the RNG.
    value = rng.randint(0, 2**128 - 1)
    return EntityId(uuid.UUID(int=value))


class Entity(Protocol):
    """Protocol all entities must implement.

    This is a structural interface: any object with these attributes is
    considered an ``Entity`` for typing purposes.
    """

    @property
    def id(self) -> EntityId:
        """Unique, immutable identifier for this entity."""

    @property
    def position(self) -> Position:
        """Current position in the world."""

    @position.setter
    def position(self, value: Position) -> None:
        """Update the entity's position."""

    @property
    def entity_type(self) -> EntityType:
        """Category of this entity for filtering/grouping."""


class BaseEntity:
    """Compatibility placeholder.

    The repository previously exported ``BaseEntity`` from ``terrarium.entities``.
    Concrete implementations are out of scope for this work order; this class
    exists only to avoid breaking imports.
    """

    pass
