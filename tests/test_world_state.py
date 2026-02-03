from __future__ import annotations

from dataclasses import dataclass

import pytest

from terrarium.world import Grid, Position, WorldState


@dataclass(frozen=True)
class DummyEntity:
    id: int
    position: Position


def test_empty_world() -> None:
    ws = WorldState(Grid(5, 5), seed=123)
    assert ws.tick == 0
    assert ws.get_entity(1) is None
    assert ws.get_entities_at(Position(0, 0)) == []


def test_add_and_get_entity_by_id() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    e = DummyEntity(id=7, position=Position(2, 3))
    ws.add_entity(e)

    assert ws.get_entity(7) is e
    assert ws.get_entities_at(Position(2, 3)) == [e]


def test_remove_entity() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    e = DummyEntity(id=1, position=Position(1, 1))
    ws.add_entity(e)

    ws.remove_entity(1)
    assert ws.get_entity(1) is None
    assert ws.get_entities_at(Position(1, 1)) == []


def test_entities_at_position_multiple() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    e1 = DummyEntity(id=1, position=Position(4, 4))
    e2 = DummyEntity(id=2, position=Position(4, 4))
    ws.add_entity(e1)
    ws.add_entity(e2)

    assert ws.get_entities_at(Position(4, 4)) == [e1, e2]


def test_positions_are_wrapped_for_queries() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    e = DummyEntity(id=1, position=Position(5, 0))  # wraps to (0,0)
    ws.add_entity(e)

    assert ws.get_entities_at(Position(0, 0)) == [e]
    assert ws.get_entities_at(Position(5, 0)) == [e]


def test_step_increments_tick() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    assert ws.tick == 0
    ws.step()
    assert ws.tick == 1
    ws.step()
    assert ws.tick == 2
