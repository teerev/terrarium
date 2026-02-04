from __future__ import annotations

import uuid

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.consumption import ConsumptionRule
from terrarium.entities.organism import create_organism
from terrarium.entities.resource import create_resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_organism_gains_energy_and_resource_removed() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    org = create_organism(Position(2, 2), energy=10)
    res = create_resource(Position(2, 2), energy_value=7)
    world.add_entity(org)
    world.add_entity(res)

    rule = ConsumptionRule()
    events = rule.apply(world, SeededRNG(0))

    assert org.energy == 17
    assert world.get_entity(res.id) is None
    assert len(events) == 1


def test_first_organism_consumes_deterministic_by_id() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    # Use explicit UUIDs to control deterministic ordering
    id1 = uuid.UUID("00000000-0000-0000-0000-000000000001")
    id2 = uuid.UUID("00000000-0000-0000-0000-000000000002")

    org1 = create_organism(Position(1, 1), energy=5, id=id1)
    org2 = create_organism(Position(1, 1), energy=5, id=id2)
    res = create_resource(Position(1, 1), energy_value=10)

    world.add_entity(org1)
    world.add_entity(org2)
    world.add_entity(res)

    rule = ConsumptionRule()
    rule.apply(world, SeededRNG(0))

    assert org1.energy == 15
    assert org2.energy == 5
    assert world.get_entity(res.id) is None
