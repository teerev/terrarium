from __future__ import annotations

"""World state container.

A minimal placeholder object representing the evolving state of the simulation.
"""

from dataclasses import dataclass

from terrarium.world.grid import Grid


@dataclass(slots=True)
class WorldState:
    """Container for world state.

    This placeholder holds a grid reference. Future versions may track entities,
    resources, time steps, and other state.
    """

    grid: Grid
