from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_zero_energy_dies_and_removed_from_indices() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    rng = SeededRNG(123)

    dead = create_organism(Position(1, 1), energy=0, rng=rng)
    alive = create_organism(Position(2, 2), energy=2, rng=rng)

    world.add_entity(dead)
    world.add_entity(alive)

    sim = Simulation(world, rng)
    sim.step()

    assert world.get_entity(dead.id) is None
    assert world.get_entity(alive.id) is alive
    assert dead not in world.get_entities_at(Position(1, 1))


def test_negative_energy_dies_via_rule() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    rng = SeededRNG(1)

    org = create_organism(Position(0, 0), energy=1, rng=rng)
    world.add_entity(org)

    # Force an invalid (negative) energy state to simulate post-update results.
    org.energy = -1

    sim = Simulation(world, rng)
    sim.step()

    assert world.get_entity(org.id) is None
