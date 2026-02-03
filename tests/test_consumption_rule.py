from __future__ import annotations

from terrarium.engine.rules.consumption import ConsumptionRule
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_consumption_transfers_energy_and_removes_resource() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    pos = Position(2, 2)

    org = Organism(position=pos, energy=3, id="org-a")
    res = Resource(position=pos, energy_value=7, id="res-a")

    world.add_entity(org)
    world.add_entity(res)

    events = ConsumptionRule().apply(world, world.rng)

    assert org.energy == 10
    assert world.get_entity(res.id) is None
    assert len(events) == 1
    assert events[0].organism_id == "org-a"
    assert events[0].resource_id == "res-a"
    assert events[0].energy_gained == 7


def test_consumption_requires_same_position() -> None:
    world = WorldState(Grid(5, 5), seed=1)

    org = Organism(position=Position(0, 0), energy=1, id="org-a")
    res = Resource(position=Position(1, 0), energy_value=5, id="res-a")

    world.add_entity(org)
    world.add_entity(res)

    events = ConsumptionRule().apply(world, world.rng)

    assert org.energy == 1
    assert world.get_entity(res.id) is not None
    assert events == []


def test_only_one_organism_consumes_each_resource_deterministic_by_id() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    pos = Position(3, 3)

    # Two organisms on the same tile: lower id should consume first.
    org1 = Organism(position=pos, energy=1, id="org-1")
    org2 = Organism(position=pos, energy=1, id="org-2")
    res = Resource(position=pos, energy_value=4, id="res-a")

    world.add_entity(org2)
    world.add_entity(res)
    world.add_entity(org1)

    events = ConsumptionRule().apply(world, world.rng)

    assert world.get_entity(res.id) is None
    assert org1.energy == 5
    assert org2.energy == 1
    assert len(events) == 1
    assert events[0].organism_id == "org-1"
