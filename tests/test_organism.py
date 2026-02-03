from __future__ import annotations

import pytest

from terrarium.entities import Entity, EntityType, create_organism, generate_id
from terrarium.world import Position


def test_organism_implements_entity_and_entity_type():
    o = create_organism(Position(1, 2), energy=3)

    assert isinstance(o, Entity)
    assert o.entity_type is EntityType.ORGANISM


def test_organism_initial_state_and_mutability():
    o = create_organism(Position(0, 0), energy=10)

    assert o.age == 0
    assert o.energy == 10
    assert o.is_alive is True

    o.energy -= 7
    assert o.energy == 3
    assert o.is_alive is True

    o.energy -= 3
    assert o.energy == 0
    assert o.is_alive is False

    o.position = Position(2, 3)
    assert o.position == Position(2, 3)


def test_organism_age_increments_on_tick():
    o = create_organism(Position(0, 0), energy=1)

    assert o.age == 0
    assert o.tick() == 1
    assert o.age == 1


def test_organism_validation_and_factory_id_behavior():
    with pytest.raises(ValueError):
        create_organism(Position(0, 0), energy=-1)

    explicit = generate_id()
    o1 = create_organism(Position(0, 0), energy=1, id=explicit)
    o2 = create_organism(Position(0, 0), energy=1)

    assert o1.id == explicit
    assert o2.id != explicit
