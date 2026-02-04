"""World state container.

This is a placeholder for a future, richer world implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.world.grid import Grid


@dataclass(slots=True)
class WorldState:
    """Holds the current world state.

    For now this is only a grid reference; later it may include entities,
    resources, and other mutable state.
    """

    grid: Grid
