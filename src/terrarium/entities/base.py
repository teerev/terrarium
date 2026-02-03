from __future__ import annotations

from enum import Enum
from typing import NewType, Protocol, runtime_checkable
from uuid import UUID, uuid4

from terrarium.world.grid import Position

# Entity IDs are UUIDs to ensure uniqueness across runs and processes.
EntityId = NewType("EntityId", UUID)


class EntityType(str, Enum):
    """High-level categories for entities.

    Used for filtering/grouping entities without relying on concrete classes.
    """

    ORGANISM = "organism"
    RESOURCE = "resource"


def generate_id() -> EntityId:
    """Generate a new unique, immutable entity identifier."""

    return EntityId(uuid4())


@runtime_checkable
class Entity(Protocol):
    """Base protocol for simulation entities.

    Contract:
    - id: unique and immutable identifier for the lifetime of the entity
    - position: gettable and settable location in the world
    - entity_type: identifies the category for filtering/dispatch

    This is a structural type (Protocol). Any object with these attributes
    satisfies the protocol, enabling composition over inheritance.
    """

    id: EntityId
    position: Position
    entity_type: EntityType
