from __future__ import annotations

import pytest

from terrarium.entities.base import Entity, EntityType
from terrarium.entities.resource import Resource, create_resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_resource_implements_entity_and_energy_value() -> None:
    r = create_resource(Position(1, 2), 10)

    # Protocol satisfaction (runtime check via structural typing)
    assert isinstance(r, Resource)
    assert isinstance(r, Entity)

    assert r.energy_value == 10
    assert r.entity_type == EntityType.RESOURCE
    # Resources are stationary; factory should preserve the provided position
    assert r.position == Position(1, 2)


def test_resource_in_world_add_and_remove() -> None:
    world = WorldState(Grid(5, 5), seed=0)
    r = create_resource(Position(4, 4), 7)

    world.add_entity(r)
    assert world.get_entity(r.id) is r
    assert r in world.get_entities_at(Position(4, 4))

    world.remove_entity(r.id)
    assert world.get_entity(r.id) is None
    assert world.get_entities_at(Position(4, 4)) == []


def test_resource_energy_value_validation() -> None:
    with pytest.raises(ValueError):
        create_resource(Position(0, 0), 0)
