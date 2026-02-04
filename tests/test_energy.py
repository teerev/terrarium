from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_metabolism_drains_energy_and_floors_at_zero() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    o1 = create_organism(Position(0, 0), energy=5)
    o2 = create_organism(Position(1, 1), energy=1)
    world.add_entity(o1)
    world.add_entity(o2)

    sim = Simulation(world=world, rng=SeededRNG(1), energy=EnergyRule(metabolism_rate=2))

    sim.step()
    assert o1.energy == 3
    assert o2.energy == 0

    sim.step()
    assert o1.energy == 1
    assert o2.energy == 0


def test_metabolism_rate_configurable_and_all_organisms_affected() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    o1 = create_organism(Position(0, 0), energy=10)
    o2 = create_organism(Position(2, 2), energy=10)
    world.add_entity(o1)
    world.add_entity(o2)

    sim = Simulation(world=world, rng=SeededRNG(2), energy=EnergyRule(metabolism_rate=3))
    sim.run(2)

    assert o1.energy == 4
    assert o2.energy == 4
