from __future__ import annotations

"""Grid data structure.

A minimal placeholder for a 2D world representation.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Grid:
    """A rectangular grid defining world dimensions.

    This placeholder only captures width/height. Future implementations may add
    terrain, occupancy, and neighborhood queries.
    """

    width: int
    height: int
