from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True, slots=True)
class Position:
    """Immutable 2D integer coordinate."""

    x: int
    y: int


class Grid:
    """A 2D toroidal grid (wrap-around at edges)."""

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = int(width)
        self.height = int(height)

    def wrap(self, pos: Position) -> Position:
        """Wrap a position into grid bounds using toroidal topology."""

        return Position(pos.x % self.width, pos.y % self.height)

    def neighbors(self, pos: Position, *, diagonals: bool = False) -> List[Position]:
        """Return neighboring positions around pos.

        If diagonals is False, returns 4-way (von Neumann) adjacency.
        If diagonals is True, returns 8-way (Moore) adjacency.
        """

        p = self.wrap(pos)
        if diagonals:
            offsets: Iterable[tuple[int, int]] = (
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
            offsets = ((0, -1), (-1, 0), (1, 0), (0, 1))

        return [self.wrap(Position(p.x + dx, p.y + dy)) for dx, dy in offsets]

    def distance(self, p1: Position, p2: Position) -> int:
        """Toroidal Manhattan distance between two positions."""

        a = self.wrap(p1)
        b = self.wrap(p2)

        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        dx = min(dx, self.width - dx)
        dy = min(dy, self.height - dy)
        return dx + dy
