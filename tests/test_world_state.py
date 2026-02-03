from __future__ import annotations

from dataclasses import dataclass

import pytest

from terrarium.core.types import EntityId, Seed
from terrarium.world import Grid, Position, WorldState


@dataclass
class DummyEntity:
    id: EntityId
    position: Position


def test_empty_world_tick_and_queries():
    world = WorldState(grid=Grid(5, 5), seed=Seed(1))

    assert world.tick == 0
    assert world.get_entity(EntityId(123)) is None
    assert world.get_entities_at(Position(0, 0)) == []


def test_add_remove_and_position_lookup_with_wrapping():
    world = WorldState(grid=Grid(3, 3), seed=Seed(2))

    e1 = DummyEntity(id=EntityId(1), position=Position(0, 0))
    e2 = DummyEntity(id=EntityId(2), position=Position(3, 0))  # wraps to (0,0)

    world.add_entity(e1)
    world.add_entity(e2)

    got = world.get_entities_at(Position(0, 0))
    assert {e.id for e in got} == {EntityId(1), EntityId(2)}
    assert world.get_entity(EntityId(2)) is e2

    world.remove_entity(EntityId(1))
    assert world.get_entity(EntityId(1)) is None
    assert {e.id for e in world.get_entities_at(Position(0, 0))} == {EntityId(2)}


def test_add_entity_duplicate_id_rejected():
    world = WorldState(grid=Grid(2, 2), seed=Seed(3))

    world.add_entity(DummyEntity(id=EntityId(1), position=Position(0, 0)))
    with pytest.raises(ValueError):
        world.add_entity(DummyEntity(id=EntityId(1), position=Position(1, 1)))
