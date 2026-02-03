"""Grid representation for the simulation world.

This module provides minimal scaffolding for a 2D grid-based world.
Implementation details will be added in later milestones.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grid:
    """A placeholder 2D grid.

    Intended to represent the topology/size of the world and provide coordinate
    utilities.
    """

    width: int
    height: int
