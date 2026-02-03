"""Entity definitions for terrarium.

The entities subpackage defines the data structures representing organisms,
resources, and other simulated actors.
"""

from __future__ import annotations

from .base import Entity, EntityId, EntityType, generate_id
from .organism import Organism, create_organism
from .resource import Resource, create_resource

__all__ = [
    "Entity",
    "EntityId",
    "EntityType",
    "generate_id",
    "Organism",
    "create_organism",
    "Resource",
    "create_resource",
]
