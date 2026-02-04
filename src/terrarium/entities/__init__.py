"""Entity definitions.

This subpackage defines domain objects for things that exist in the world, such
as organisms and resources.
"""

from __future__ import annotations

from .base import Entity, EntityId, EntityType, generate_id
from .organism import Organism
from .resource import Resource

__all__ = [
    "Entity",
    "EntityId",
    "EntityType",
    "generate_id",
    "Organism",
    "Resource",
]
