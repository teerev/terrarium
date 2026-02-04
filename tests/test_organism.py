from __future__ import annotations

from terrarium.entities import Entity, EntityType, Organism, create_organism
from terrarium.world.grid import Position


def test_organism_implements_entity_and_fields_mutable() -> None:
    org = create_organism(Position(1, 2), energy=10)

    # Protocol check (runtime_checkable)
    assert isinstance(org, Entity)
    assert org.entity_type == EntityType.ORGANISM

    # age starts at 0
    assert org.age == 0

    # energy is readable and modifiable
    org.energy -= 3
    assert org.energy == 7

    # position is mutable
    org.position = Position(3, 4)
    assert org.position == Position(3, 4)


def test_organism_initial_energy_and_is_alive() -> None:
    org = Organism(position=Position(0, 0), energy=1, id=create_organism(Position(0, 0), energy=1).id)
    assert org.energy == 1
    assert org.is_alive is True

    org.energy = 0
    assert org.is_alive is False
