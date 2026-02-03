from __future__ import annotations

import pytest

from terrarium.core.types import Seed
from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules import EnergyRule
from terrarium.entities import create_organism
from terrarium.world import Grid, Position, WorldState


def test_metabolism_drains_energy_and_multiple_ticks_cumulative():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))
    o = create_organism(Position(1, 1), energy=10)
    world.add_entity(o)

    sim = Simulation(
        world=world,
        rng=SeededRNG(seed=123),
        energy_rule=EnergyRule(metabolism_rate=2),
    )

    sim.step()
    assert o.energy == 8

    sim.run(3)
    assert world.tick == 4
    assert o.energy == 2


def test_energy_floors_at_zero_and_all_organisms_affected():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))
    o1 = create_organism(Position(0, 0), energy=1)
    o2 = create_organism(Position(2, 2), energy=5)
    world.add_entity(o1)
    world.add_entity(o2)

    sim = Simulation(
        world=world,
        rng=SeededRNG(seed=999),
        energy_rule=EnergyRule(metabolism_rate=3),
    )

    sim.step()
    assert o1.energy == 0
    assert o2.energy == 2

    sim.step()
    assert o1.energy == 0
    assert o2.energy == 0


def test_metabolism_rate_configurable():
    world_a = WorldState(grid=Grid(2, 2), seed=Seed(1))
    world_b = WorldState(grid=Grid(2, 2), seed=Seed(1))

    oa = create_organism(Position(0, 0), energy=10)
    ob = create_organism(Position(0, 0), energy=10)
    world_a.add_entity(oa)
    world_b.add_entity(ob)

    sim_a = Simulation(world=world_a, rng=SeededRNG(seed=1), energy_rule=EnergyRule(1))
    sim_b = Simulation(world=world_b, rng=SeededRNG(seed=1), energy_rule=EnergyRule(4))

    sim_a.step()
    sim_b.step()

    assert oa.energy == 9
    assert ob.energy == 6


def test_energy_rule_validates_non_negative_rate():
    with pytest.raises(ValueError):
        EnergyRule(metabolism_rate=-1)
