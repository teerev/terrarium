"""Entity definitions.

This subpackage contains entity contracts and concrete entity types used by the simulation.

Public APIs:
- Entity: Protocol defining the entity interface
- EntityId: Type alias for entity identifiers
- EntityType: Enum of entity categories
- generate_id: Utility to generate unique entity IDs
"""

from __future__ import annotations

from .base import Entity, EntityId, EntityType, generate_id

__all__ = ["Entity", "EntityId", "EntityType", "generate_id"]
