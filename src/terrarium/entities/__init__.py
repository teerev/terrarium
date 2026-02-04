"""Entity definitions.

This subpackage contains entity interfaces and (optionally) concrete entity
types such as organisms and resources.
"""

from __future__ import annotations

from .base import BaseEntity, Entity, EntityId, EntityType, generate_id

__all__ = [
    "BaseEntity",
    "Entity",
    "EntityId",
    "EntityType",
    "generate_id",
]
