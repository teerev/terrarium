from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Immutable 2D integer grid coordinate."""

    x: int
    y: int


class Grid:
    """Toroidal 2D grid.

    Coordinates wrap around at edges (toroidal topology).
    All operations are pure: methods return new Position values.
    """

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Grid width and height must be positive")
        self.width = width
        self.height = height

    def wrap(self, pos: Position) -> Position:
        """Return position wrapped into grid bounds."""
        return Position(pos.x % self.width, pos.y % self.height)

    def neighbors(self, pos: Position, *, diagonals: bool = False) -> list[Position]:
        """Return wrapped adjacent positions.

        By default returns 4-way (von Neumann) adjacency.
        If diagonals=True, returns 8-way (Moore) adjacency.
        """
        if diagonals:
            offsets = (
                (-1, -1),
                (0, -1),
                (1, -1),
                (-1, 0),
                (1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
            )
        else:
            offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))

        return [self.wrap(Position(pos.x + dx, pos.y + dy)) for dx, dy in offsets]

    def distance(self, p1: Position, p2: Position) -> int:
        """Toroidal Manhattan distance between two positions."""
        a = self.wrap(p1)
        b = self.wrap(p2)

        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)

        dx = min(dx, self.width - dx)
        dy = min(dy, self.height - dy)
        return dx + dy
