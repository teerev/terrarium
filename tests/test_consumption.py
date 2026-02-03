from __future__ import annotations

from uuid import UUID

from terrarium.core.types import Seed
from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules import ConsumptionRule
from terrarium.entities import create_organism, create_resource
from terrarium.world import Grid, Position, WorldState


def test_organism_gains_energy_and_resource_removed_when_same_position():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))
    org = create_organism(Position(1, 1), energy=2)
    res = create_resource(Position(1, 1), energy_value=7)
    world.add_entity(org)
    world.add_entity(res)

    sim = Simulation(
        world=world,
        rng=SeededRNG(seed=123),
        consumption_rule=ConsumptionRule(),
    )

    sim.step()

    assert org.energy == 9
    assert world.get_entity(res.id) is None


def test_no_resource_no_gain_and_position_must_match():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))
    org = create_organism(Position(0, 0), energy=5)
    res = create_resource(Position(1, 0), energy_value=10)
    world.add_entity(org)
    world.add_entity(res)

    sim = Simulation(world=world, rng=SeededRNG(seed=1), consumption_rule=ConsumptionRule())
    sim.step()

    assert org.energy == 5
    assert world.get_entity(res.id) is res


def test_first_organism_by_id_consumes_only_one_resource_per_tick():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))

    # Create deterministic, ordered IDs (UUID comparison by str is deterministic here).
    id1 = UUID("00000000-0000-0000-0000-000000000001")
    id2 = UUID("00000000-0000-0000-0000-000000000002")

    o1 = create_organism(Position(2, 2), energy=1, id=id1)
    o2 = create_organism(Position(2, 2), energy=1, id=id2)
    r = create_resource(Position(2, 2), energy_value=4)

    world.add_entity(o2)
    world.add_entity(r)
    world.add_entity(o1)

    sim = Simulation(world=world, rng=SeededRNG(seed=99), consumption_rule=ConsumptionRule())
    sim.step()

    assert o1.energy == 5
    assert o2.energy == 1
    assert world.get_entity(r.id) is None
