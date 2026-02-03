"""Spatial grid primitives.

This module defines the 2D grid coordinate system used by the world model.

Design constraints
------------------
- Integer coordinates for determinism.
- Toroidal topology: edges wrap-around.
- Operations are pure: methods return new values and do not mutate inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal


@dataclass(frozen=True, slots=True)
class Position:
    """Immutable 2D integer coordinate pair in (x, y) order."""

    x: int
    y: int


Adjacency = Literal[4, 8]


@dataclass(frozen=True, slots=True)
class Grid:
    """A discrete 2D grid with toroidal wrapping."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Grid width and height must be positive integers")

    def wrap(self, pos: Position) -> Position:
        """Wrap a position onto the grid using toroidal topology."""

        return Position(pos.x % self.width, pos.y % self.height)

    def neighbors(self, pos: Position, *, adjacency: Adjacency = 4) -> list[Position]:
        """Return wrapped neighbor positions.

        Parameters
        ----------
        pos:
            Source position.
        adjacency:
            4 for Von Neumann neighborhood, 8 for Moore neighborhood.

        Returns
        -------
        list[Position]
            Neighbor positions in a stable order.
        """

        if adjacency not in (4, 8):
            raise ValueError("adjacency must be 4 or 8")

        offsets: Iterable[tuple[int, int]]
        offsets = ((1, 0), (-1, 0), (0, 1), (0, -1))
        if adjacency == 8:
            offsets = (
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1),
                (1, 1),
                (1, -1),
                (-1, 1),
                (-1, -1),
            )

        return [self.wrap(Position(pos.x + dx, pos.y + dy)) for dx, dy in offsets]

    def distance(self, a: Position, b: Position) -> int:
        """Toroidal Manhattan distance between two positions."""

        ax, ay = self.wrap(a).x, self.wrap(a).y
        bx, by = self.wrap(b).x, self.wrap(b).y

        dx = abs(ax - bx)
        dy = abs(ay - by)

        dx = min(dx, self.width - dx)
        dy = min(dy, self.height - dy)

        return int(dx + dy)
