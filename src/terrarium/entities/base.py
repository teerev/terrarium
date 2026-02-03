"""Base entity types.

Concrete entities (organisms, resources, etc.) should build on these shared
definitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import EntityId


@dataclass(slots=True)
class Entity:
    """A minimal base class for any world entity."""

    id: EntityId
