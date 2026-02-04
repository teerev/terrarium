from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.types import EntityId
from terrarium.world import Grid
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class DummyEntity:
    id: EntityId
    position: Position


def test_empty_world() -> None:
    ws = WorldState(Grid(5, 5), seed=123)
    assert ws.tick == 0
    assert ws.get_entities_at(Position(0, 0)) == []


def test_add_get_remove_entity_and_position_index() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    e1 = DummyEntity(EntityId("e1"), Position(1, 2))
    e2 = DummyEntity(EntityId("e2"), Position(1, 2))

    ws.add_entity(e1)
    ws.add_entity(e2)

    assert ws.get_entity(EntityId("e1")) is e1
    assert ws.get_entity(EntityId("e2")) is e2

    at = ws.get_entities_at(Position(1, 2))
    assert set(at) == {e1, e2}

    ws.remove_entity(EntityId("e1"))
    assert ws.get_entity(EntityId("e1")) is None
    assert ws.get_entities_at(Position(1, 2)) == [e2] or set(ws.get_entities_at(Position(1, 2))) == {e2}
