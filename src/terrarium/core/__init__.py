"""Core shared types and protocols.

This subpackage defines foundational, dependency-light types and interfaces
used across the simulation (world, entities, and engine).
"""

from __future__ import annotations

from .protocols import HasId, SupportsRng
from .types import EntityId, Position

__all__ = [
    "EntityId",
    "Position",
    "HasId",
    "SupportsRng",
]
