"""World state container.

This module provides a minimal placeholder object representing the full world
state at a point in time.
"""

from __future__ import annotations

from dataclasses import dataclass

from .grid import Grid


@dataclass(slots=True)
class WorldState:
    """Aggregate of world-level state for the simulation.

    Placeholder: will later include entities, resources, and other global state.
    """

    grid: Grid
