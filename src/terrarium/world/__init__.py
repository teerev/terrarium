"""World state management.

This subpackage defines structures representing the simulation world (e.g., a
grid) and the evolving state over time.
"""

from __future__ import annotations

from .grid import Grid, Position
from .state import WorldState

__all__ = ["Grid", "Position", "WorldState"]
