from __future__ import annotations

from terrarium.world import Grid, Position


def test_position_equality_and_hashable() -> None:
    p1 = Position(1, 2)
    p2 = Position(1, 2)
    assert p1 == p2

    s = {p1}
    assert p2 in s


def test_wrap_out_of_bounds() -> None:
    g = Grid(width=5, height=3)
    assert g.wrap(Position(5, 0)) == Position(0, 0)
    assert g.wrap(Position(-1, 0)) == Position(4, 0)
    assert g.wrap(Position(0, 3)) == Position(0, 0)
    assert g.wrap(Position(0, -1)) == Position(0, 2)


def test_neighbors_count_and_wrapped() -> None:
    g = Grid(width=4, height=4)

    n4 = g.neighbors(Position(0, 0))
    assert len(n4) == 4
    assert Position(3, 0) in n4
    assert Position(0, 3) in n4

    n8 = g.neighbors(Position(0, 0), diagonals=True)
    assert len(n8) == 8
    assert Position(3, 3) in n8


def test_distance_toroidal_manhattan() -> None:
    g = Grid(width=10, height=10)
    assert g.distance(Position(0, 0), Position(9, 0)) == 1
    assert g.distance(Position(0, 0), Position(9, 9)) == 2
