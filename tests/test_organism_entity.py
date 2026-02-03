from __future__ import annotations

import pytest

from terrarium.entities.base import EntityType
from terrarium.entities.organism import Organism, create_organism
from terrarium.world.grid import Position


def test_create_organism_and_basic_properties() -> None:
    org = create_organism(Position(1, 2), 10)
    assert isinstance(org, Organism)
    assert org.entity_type == EntityType.ORGANISM
    assert org.energy == 10
    assert org.age == 0
    assert org.position == Position(1, 2)


def test_organism_mutable_position_energy_and_age_tick() -> None:
    org = Organism(Position(0, 0), 1)

    org.position = Position(3, 4)
    assert org.position == Position(3, 4)

    org.energy = 7
    assert org.energy == 7

    assert org.is_alive is True

    org.tick()
    org.tick()
    assert org.age == 2


def test_organism_energy_non_negative() -> None:
    with pytest.raises(ValueError):
        Organism(Position(0, 0), -1)

    org = Organism(Position(0, 0), 0)
    assert org.is_alive is False

    with pytest.raises(ValueError):
        org.energy = -5
