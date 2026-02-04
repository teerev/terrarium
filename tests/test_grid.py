from __future__ import annotations

from terrarium.world.grid import Grid, Position


def test_position_hashable():
    p = Position(1, 2)
    d = {p: "ok"}
    assert d[Position(1, 2)] == "ok"


def test_wrap():
    g = Grid(10, 10)
    assert g.wrap(Position(0, 0)) == Position(0, 0)
    assert g.wrap(Position(10, 0)) == Position(0, 0)
    assert g.wrap(Position(-1, 0)) == Position(9, 0)
    assert g.wrap(Position(0, -2)) == Position(0, 8)


def test_neighbors_4_and_8_are_wrapped():
    g = Grid(3, 3)
    p = Position(0, 0)

    n4 = set(g.neighbors(p, diagonals=False))
    assert n4 == {
        Position(1, 0),
        Position(2, 0),
        Position(0, 1),
        Position(0, 2),
    }

    n8 = set(g.neighbors(p, diagonals=True))
    assert len(n8) == 8
    assert Position(2, 2) in n8


def test_toroidal_distance_manhattan():
    g = Grid(10, 10)
    assert g.distance(Position(0, 0), Position(9, 0)) == 1
    assert g.distance(Position(0, 0), Position(0, 9)) == 1
    assert g.distance(Position(0, 0), Position(9, 9)) == 2
