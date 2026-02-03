"""Spatial grid primitives.

This module defines a minimal placeholder grid type. It intentionally avoids
simulation logic and only establishes a stable interface.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grid:
    """A discrete 2D grid backing the world.

    Placeholder: in future iterations this will likely manage occupancy,
    boundaries, and neighborhood queries.
    """

    width: int
    height: int
