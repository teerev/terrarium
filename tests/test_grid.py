from __future__ import annotations

import pytest

from terrarium.world import Grid, Position


def test_position_equality_and_hashable():
    p1 = Position(1, 2)
    p2 = Position(1, 2)
    p3 = Position(2, 1)

    assert p1 == p2
    assert p1 != p3

    s = {p1, p2, p3}
    assert len(s) == 2

    d = {p1: "a", p3: "b"}
    assert d[Position(1, 2)] == "a"
    assert d[Position(2, 1)] == "b"


def test_wrap_in_bounds_and_out_of_bounds():
    g = Grid(width=5, height=3)

    assert g.wrap(Position(0, 0)) == Position(0, 0)
    assert g.wrap(Position(4, 2)) == Position(4, 2)

    assert g.wrap(Position(5, 0)) == Position(0, 0)
    assert g.wrap(Position(-1, 0)) == Position(4, 0)
    assert g.wrap(Position(0, 3)) == Position(0, 0)
    assert g.wrap(Position(0, -1)) == Position(0, 2)


def test_neighbors_count_and_wrapping_for_4_way():
    g = Grid(width=3, height=3)
    ns = g.neighbors(Position(0, 0), adjacency=4)

    assert len(ns) == 4
    assert set(ns) == {
        Position(1, 0),
        Position(2, 0),  # -1 wraps to 2
        Position(0, 1),
        Position(0, 2),  # -1 wraps to 2
    }


def test_neighbors_count_for_8_way_and_validation():
    g = Grid(width=10, height=10)

    ns8 = g.neighbors(Position(5, 5), adjacency=8)
    assert len(ns8) == 8
    assert len(set(ns8)) == 8

    with pytest.raises(ValueError):
        g.neighbors(Position(0, 0), adjacency=7)  # type: ignore[arg-type]


def test_distance_toroidal_manhattan():
    g = Grid(width=10, height=10)

    assert g.distance(Position(0, 0), Position(3, 4)) == 7

    # Wrap-around should be shorter across boundary.
    assert g.distance(Position(0, 0), Position(9, 0)) == 1
    assert g.distance(Position(0, 0), Position(0, 9)) == 1

    # Symmetry
    assert g.distance(Position(9, 0), Position(0, 0)) == 1


def test_grid_dimensions_must_be_positive():
    with pytest.raises(ValueError):
        Grid(width=0, height=1)
    with pytest.raises(ValueError):
        Grid(width=1, height=-1)
