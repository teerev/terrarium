from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import EntityId
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


@dataclass(frozen=True)
class _E:
    _id: EntityId
    _pos: Position

    @property
    def id(self) -> EntityId:
        return self._id

    @property
    def position(self) -> Position:
        return self._pos


def test_world_state_initializes_empty_and_tick_zero() -> None:
    w = WorldState(Grid(5, 5), seed=1)
    assert w.tick == 0
    assert w.get_entity(EntityId("missing")) is None
    assert w.get_entities_at(Position(0, 0)) == []


def test_add_get_remove_entity_and_position_lookup_wraps_positions() -> None:
    w = WorldState(Grid(5, 5), seed=1)

    # WorldState stores entities at wrapped positions (toroidal grid).
    e1 = _E(EntityId("e1"), Position(2, 3))
    e2 = _E(EntityId("e2"), Position(7, 8))  # wraps to (2,3)

    w.add_entity(e1)
    w.add_entity(e2)

    assert w.get_entity(EntityId("e1")) is e1
    assert w.get_entity(EntityId("e2")) is e2

    at = w.get_entities_at(Position(2, 3))
    assert set(at) == {e1, e2}

    w.remove_entity(EntityId("e1"))
    assert w.get_entity(EntityId("e1")) is None
    assert w.get_entities_at(Position(2, 3)) == [e2]


def test_step_increments_tick() -> None:
    w = WorldState(Grid(2, 2), seed=1)
    assert w.tick == 0
    assert w.step() == 1
    assert w.tick == 1
