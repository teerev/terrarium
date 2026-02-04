from __future__ import annotations

"""Base entity protocol.

This module defines the minimal interface (contract) that all simulation entities
must implement.

Design notes:
- The `Entity` type is a `typing.Protocol` to support structural subtyping.
- Entity IDs are generated via `generate_id()` and are intended to be immutable.
- `position` must be readable and writable so the world/engine can move entities.
- `entity_type` allows filtering/grouping entities by category.

Public APIs:
- EntityId: type alias for stable entity identifiers
- EntityType: enum of entity categories
- generate_id(): create a new unique EntityId
- Entity: protocol defining the required entity interface
"""

import uuid
from enum import Enum
from typing import Protocol, runtime_checkable

from terrarium.world.grid import Position


EntityId = uuid.UUID
"""Stable identifier for an entity within a simulation.

Entity IDs are UUIDs to ensure uniqueness across runs and processes.
"""


class EntityType(str, Enum):
    """High-level entity category for filtering/dispatch."""

    ORGANISM = "ORGANISM"
    RESOURCE = "RESOURCE"


def generate_id() -> EntityId:
    """Return a new unique entity ID."""

    return uuid.uuid4()


@runtime_checkable
class Entity(Protocol):
    """Structural protocol that all entities must satisfy.

    Required attributes:
    - id: unique, immutable entity identifier
    - position: current position in the world (gettable and settable)
    - entity_type: category identifier for filtering
    """

    id: EntityId
    position: Position
    entity_type: EntityType
