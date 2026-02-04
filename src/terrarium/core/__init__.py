"""Core shared types and protocols for Terrarium.

This subpackage contains small, dependency-light building blocks (type aliases,
Protocols) that higher-level subpackages can depend on without creating circular
imports.
"""

from __future__ import annotations

from .protocols import Entity, RandomSource, World
from .types import EntityId, Position

__all__ = [
    "EntityId",
    "Position",
    "Entity",
    "World",
    "RandomSource",
]
