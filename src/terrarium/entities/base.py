"""Base entity types.

This module provides minimal concrete implementations that can satisfy core
protocols while the simulation logic is developed.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import EntityId, Position


@dataclass(frozen=True, slots=True)
class BaseEntity:
    """Minimal concrete entity.

    Acts as a simple, typed placeholder that can be stored in a world.
    """

    id: EntityId
    position: Position
