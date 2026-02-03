from __future__ import annotations

from terrarium.world import Grid, Position


def test_position_equality_and_hashable() -> None:
    p1 = Position(1, 2)
    p2 = Position(1, 2)
    p3 = Position(2, 1)

    assert p1 == p2
    assert p1 != p3

    s = {p1, p2, p3}
    assert len(s) == 2

    d = {p1: "a"}
    assert d[p2] == "a"


def test_wrap_in_bounds_and_out_of_bounds() -> None:
    g = Grid(width=5, height=3)

    assert g.wrap(Position(0, 0)) == Position(0, 0)
    assert g.wrap(Position(4, 2)) == Position(4, 2)

    # positive overflow
    assert g.wrap(Position(5, 3)) == Position(0, 0)
    assert g.wrap(Position(6, 4)) == Position(1, 1)

    # negative coordinates
    assert g.wrap(Position(-1, -1)) == Position(4, 2)
    assert g.wrap(Position(-6, -4)) == Position(4, 2)


def test_neighbors_count_and_wrapping() -> None:
    g = Grid(width=5, height=3)

    n4 = g.neighbors(Position(0, 0))
    assert len(n4) == 4
    assert Position(0, 2) in n4  # up wraps
    assert Position(4, 0) in n4  # left wraps

    n8 = g.neighbors(Position(0, 0), diagonals=True)
    assert len(n8) == 8
    assert Position(4, 2) in n8  # up-left wraps
    assert Position(1, 1) in n8  # down-right


def test_toroidal_distance_manhattan() -> None:
    g = Grid(width=10, height=10)

    assert g.distance(Position(0, 0), Position(0, 0)) == 0
    assert g.distance(Position(0, 0), Position(3, 0)) == 3

    # wrap-around is shorter: 0 -> 9 is distance 1 on width 10
    assert g.distance(Position(0, 0), Position(9, 0)) == 1

    # both axes
    assert g.distance(Position(0, 0), Position(9, 9)) == 2
