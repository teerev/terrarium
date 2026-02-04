"""Grid representation for the simulation.

This is a placeholder type for a future grid implementation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grid:
    """A 2D grid definition.

    This placeholder stores only dimensions. Future versions may store terrain,
    occupancy, or cell metadata.
    """

    width: int
    height: int
