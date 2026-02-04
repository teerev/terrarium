from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.death import DeathRule
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_death_rule_removes_organisms_with_zero_energy() -> None:
    world = WorldState(grid=Grid(3, 3), seed=123)
    rng = SeededRNG(123)

    o1 = create_organism(Position(0, 0), energy=1, rng=rng)
    o2 = create_organism(Position(1, 0), energy=5, rng=rng)
    world.add_entity(o1)
    world.add_entity(o2)

    sim = Simulation(world=world, rng=rng, energy_rule=EnergyRule(metabolism_rate=1), death_rule=DeathRule())
    sim.step()

    assert world.get_entity(o1.id) is None
    assert world.get_entity(o2.id) is not None

    entities = getattr(world, "_entities", {})
    assert len(entities) == 1
