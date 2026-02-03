"""World state container.

This module defines a lightweight container for world state.
"""

from __future__ import annotations

from dataclasses import dataclass

from .grid import Grid


@dataclass(frozen=True, slots=True)
class WorldState:
    """Immutable snapshot of world state.

    The internal representation will evolve; for now it contains only the grid.
    """

    grid: Grid
