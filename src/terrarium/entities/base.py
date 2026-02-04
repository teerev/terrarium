from __future__ import annotations

"""Base entity definitions.

Entities are objects that can exist in the simulation world.
"""

from dataclasses import dataclass

from terrarium.core.types import EntityId


@dataclass(slots=True)
class Entity:
    """Base class for all entities.

    This placeholder defines a stable identifier only.
    """

    id: EntityId
