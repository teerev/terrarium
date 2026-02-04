"""Shared type aliases used across the simulation.

These aliases are intentionally small and stable to support strict type-checking
without introducing heavy dependencies.
"""

from __future__ import annotations

from typing import NewType, Tuple

EntityId = NewType("EntityId", int)
"""A stable identifier for an entity within a world."""

Position = Tuple[int, int]
"""A 2D grid coordinate in (x, y) order."""
