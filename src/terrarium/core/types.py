"""Shared type aliases used across terrarium.

These types are intentionally small and stable to reduce coupling between
subsystems.
"""

from __future__ import annotations

from typing import NewType, Tuple

EntityId = NewType("EntityId", int)
"""A stable identifier for an entity within a simulation run."""

Coordinate = Tuple[int, int]
"""A grid coordinate in (x, y) order."""

Seed = NewType("Seed", int)
"""A seed value for deterministic random number generation."""
