"""Core types and protocols for terrarium.

The core subpackage contains shared type aliases and Protocol-based interfaces
used across the simulation. No simulation logic should live here.
"""

from __future__ import annotations

from .protocols import HasPosition, RandomSource
from .types import Coordinate, EntityId, Seed

__all__ = [
    "Coordinate",
    "EntityId",
    "Seed",
    "HasPosition",
    "RandomSource",
]
