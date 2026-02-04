"""2D toroidal grid coordinate system.

This module defines the coordinate and grid operations used by the world model.
All operations are pure and deterministic, using integer coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, List


@dataclass(frozen=True, slots=True)
class Position:
    """Immutable 2D integer coordinate in (x, y) order."""

    x: int
    y: int


class Grid:
    """A 2D toroidal grid with integer coordinates."""

    _OFFSETS_4 = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )

    _OFFSETS_8 = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError("Grid width and height must be positive")
        self.width = int(width)
        self.height = int(height)

    def wrap(self, pos: Position) -> Position:
        """Wrap a position into the grid bounds (toroidal topology)."""

        return Position(pos.x % self.width, pos.y % self.height)

    def neighbors(self, pos: Position, *, diagonals: bool = True) -> List[Position]:
        """Return adjacent wrapped positions.

        Args:
            pos: Center position.
            diagonals: If True, use 8-way adjacency; otherwise 4-way.
        """

        offsets = self._OFFSETS_8 if diagonals else self._OFFSETS_4
        x0, y0 = pos.x, pos.y
        return [self.wrap(Position(x0 + dx, y0 + dy)) for dx, dy in offsets]

    def neighbors4(self, pos: Position) -> List[Position]:
        """Convenience for 4-way adjacency."""

        return self.neighbors(pos, diagonals=False)

    def neighbors8(self, pos: Position) -> List[Position]:
        """Convenience for 8-way adjacency."""

        return self.neighbors(pos, diagonals=True)

    def _toroidal_delta(self, a: int, b: int, size: int) -> int:
        """Minimum absolute delta between two coordinates on a ring of `size`."""

        d = abs(a - b)
        return min(d, size - d)

    def distance(self, p1: Position, p2: Position) -> int:
        """Toroidal Manhattan distance between two positions."""

        dx = self._toroidal_delta(p1.x, p2.x, self.width)
        dy = self._toroidal_delta(p1.y, p2.y, self.height)
        return dx + dy

    def distance_euclidean(self, p1: Position, p2: Position) -> float:
        """Toroidal Euclidean distance between two positions."""

        dx = self._toroidal_delta(p1.x, p2.x, self.width)
        dy = self._toroidal_delta(p1.y, p2.y, self.height)
        return math.hypot(dx, dy)

    def iter_positions(self) -> Iterable[Position]:
        """Iterate all positions in the grid."""

        for y in range(self.height):
            for x in range(self.width):
                yield Position(x, y)
