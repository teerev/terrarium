"""World state container.

This module defines a placeholder for the mutable (or versioned) state that the
engine will advance.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.world.grid import Grid


@dataclass(slots=True)
class WorldState:
    """A placeholder container for world state.

    In the future, this will track entities, resources, and any global world
    parameters.
    """

    grid: Grid
