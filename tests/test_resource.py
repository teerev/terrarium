from __future__ import annotations

import pytest

from terrarium.core.types import Seed
from terrarium.entities import Entity, EntityType, create_resource, generate_id
from terrarium.world import Grid, Position, WorldState


def test_resource_implements_entity_and_entity_type():
    r = create_resource(Position(1, 2), energy_value=5)

    assert isinstance(r, Entity)
    assert r.entity_type is EntityType.RESOURCE


def test_resource_energy_value_and_validation():
    r = create_resource(Position(0, 0), energy_value=10)
    assert r.energy_value == 10

    with pytest.raises(ValueError):
        create_resource(Position(0, 0), energy_value=0)

    with pytest.raises(ValueError):
        create_resource(Position(0, 0), energy_value=-3)


def test_resource_factory_allows_explicit_id_and_generates_when_missing():
    explicit = generate_id()
    r1 = create_resource(Position(0, 0), energy_value=1, id=explicit)
    r2 = create_resource(Position(0, 0), energy_value=1)

    assert r1.id == explicit
    assert r2.id != explicit


def test_resource_consumption_and_world_remove():
    world = WorldState(grid=Grid(5, 5), seed=Seed(1))
    r = create_resource(Position(2, 2), energy_value=7)

    world.add_entity(r)
    assert world.get_entity(r.id) is r
    assert r.consumed is False

    gained = r.consume()
    assert gained == 7
    assert r.consumed is True

    world.remove_entity(r.id)
    assert world.get_entity(r.id) is None

    with pytest.raises(RuntimeError):
        r.consume()
