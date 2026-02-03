"""World state for terrarium.

The world subpackage owns the simulation's spatial representation and state.
Concrete world implementations may evolve over time (e.g., grid, continuous).
"""

from __future__ import annotations

from .grid import Grid, Position
from .state import WorldState

__all__ = ["Grid", "Position", "WorldState"]
