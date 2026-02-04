from __future__ import annotations

"""Resource entity.

A minimal placeholder for a consumable or collectible entity.
"""

from dataclasses import dataclass

from terrarium.entities.base import Entity


@dataclass(slots=True)
class Resource(Entity):
    """A world resource.

    Future implementations may include quantity, decay, and regeneration.
    """
