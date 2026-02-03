from __future__ import annotations

import pytest

from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.simulation import Simulation
from terrarium.engine.rng import SeededRNG
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_energy_rule_applies_metabolism_and_floors_at_zero() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    a = Organism(position=Position(0, 0), energy=5)
    b = Organism(position=Position(1, 0), energy=2)

    rule = EnergyRule(metabolism_rate=3)
    rule.apply([a, b], world)

    assert a.energy == 2
    assert b.energy == 0


def test_energy_rule_metabolism_rate_is_configurable_and_non_negative() -> None:
    with pytest.raises(ValueError):
        EnergyRule(metabolism_rate=-1)

    world = WorldState(Grid(2, 2), seed=1)
    org = Organism(position=Position(0, 0), energy=1)

    EnergyRule(metabolism_rate=0).apply([org], world)
    assert org.energy == 1


def test_simulation_step_integrates_energy_drain() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    rng = SeededRNG(1)

    org = Organism(position=Position(0, 0), energy=4)
    world.add_entity(org)

    sim = Simulation(world, rng, energy_rule=EnergyRule(metabolism_rate=2))
    sim.step()

    assert org.energy == 2
    assert world.tick == 1
