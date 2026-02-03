"""Core shared types and protocols.

This subpackage defines the foundational interfaces and type aliases used by
higher-level subpackages (world/entities/engine).
"""

from __future__ import annotations

from .protocols import Entity, RandomSource
from .types import Coord, EntityId

__all__ = ["Coord", "EntityId", "Entity", "RandomSource"]
