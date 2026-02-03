from __future__ import annotations

from terrarium.world.grid import Grid, Position


def test_position_hashable() -> None:
    d = {Position(1, 2): "ok"}
    assert d[Position(1, 2)] == "ok"


def test_wrap_out_of_bounds() -> None:
    g = Grid(10, 10)
    assert g.wrap(Position(10, 10)) == Position(0, 0)
    assert g.wrap(Position(-1, -1)) == Position(9, 9)
    assert g.wrap(Position(21, -11)) == Position(1, 9)


def test_neighbors_4_way_wraps() -> None:
    g = Grid(3, 3)
    n = set(g.neighbors(Position(0, 0)))
    assert n == {
        Position(1, 0),
        Position(2, 0),
        Position(0, 1),
        Position(0, 2),
    }


def test_neighbors_8_way_count() -> None:
    g = Grid(10, 10)
    n = g.neighbors(Position(5, 5), diagonal=True)
    assert len(n) == 8
    assert len(set(n)) == 8


def test_distance_toroidal_manhattan() -> None:
    g = Grid(10, 10)
    # across edge: (0,0) to (9,0) is 1 step
    assert g.distance(Position(0, 0), Position(9, 0)) == 1
    # wrap in y too
    assert g.distance(Position(0, 0), Position(9, 9)) == 2
