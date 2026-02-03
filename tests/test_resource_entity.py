from __future__ import annotations

import pytest

from terrarium.entities.base import EntityType
from terrarium.entities.resource import Resource, create_resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_resource_entity_protocol_fields() -> None:
    r = Resource(position=Position(1, 2), energy_value=5)
    assert r.id
    assert r.position == Position(1, 2)
    assert r.entity_type == EntityType.RESOURCE
    assert r.energy_value == 5
    assert r.consumed is False


def test_create_resource_generates_valid_id() -> None:
    r = create_resource(Position(0, 0), 3)
    assert isinstance(r, Resource)
    assert r.id


def test_worldstate_add_and_remove_resource() -> None:
    ws = WorldState(Grid(5, 5), seed=1)
    r = Resource(position=Position(4, 4), energy_value=2)

    ws.add_entity(r)
    assert ws.get_entity(r.id) is r
    assert ws.get_entities_at(Position(4, 4)) == [r]

    ws.remove_entity(r.id)
    assert ws.get_entity(r.id) is None
    assert ws.get_entities_at(Position(4, 4)) == []


def test_resource_energy_value_must_be_positive() -> None:
    with pytest.raises(ValueError):
        Resource(position=Position(0, 0), energy_value=0)
