from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """Immutable integer grid position."""

    x: int
    y: int


class Grid:
    """A 2D toroidal grid with integer coordinates."""

    _OFFSETS_4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
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

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = int(width)
        self.height = int(height)

    def wrap(self, pos: Position) -> Position:
        """Wrap a position onto the grid using toroidal topology."""

        return Position(pos.x % self.width, pos.y % self.height)

    def neighbors(self, pos: Position, *, diagonal: bool = False) -> list[Position]:
        """Return neighboring positions around pos.

        If diagonal=False: 4-way adjacency (Von Neumann neighborhood)
        If diagonal=True: 8-way adjacency (Moore neighborhood)
        """

        base = self.wrap(pos)
        offsets = self._OFFSETS_8 if diagonal else self._OFFSETS_4
        return [self.wrap(Position(base.x + dx, base.y + dy)) for dx, dy in offsets]

    def distance(self, p1: Position, p2: Position) -> int:
        """Toroidal Manhattan distance between two positions."""

        a = self.wrap(p1)
        b = self.wrap(p2)

        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)

        dx = min(dx, self.width - dx)
        dy = min(dy, self.height - dy)

        return dx + dy
