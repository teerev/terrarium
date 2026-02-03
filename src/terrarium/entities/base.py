"""Base entity definitions.

Entities are modeled as lightweight data objects. Behavior will be introduced
later via systems/engine code rather than being embedded here.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import Coordinate, EntityId


@dataclass(slots=True)
class Entity:
    """Base class for all entities in the simulation.

    Placeholder: provides identity and position only.
    """

    id: EntityId
    position: Coordinate
