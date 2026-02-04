"""World state management.

This subpackage is responsible for representing and mutating the simulation
world (e.g., a grid, terrain, and spatial queries).
"""

from __future__ import annotations

from .grid import Grid
from .state import WorldState

__all__ = [
    "Grid",
    "WorldState",
]
