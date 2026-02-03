"""Grid abstraction.

A grid provides spatial indexing for the world. Concrete storage and algorithms
are out of scope for this placeholder.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grid:
    """A minimal grid definition.

    Stores world dimensions. Spatial queries will be added in later milestones.
    """

    width: int
    height: int
