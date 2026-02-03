from __future__ import annotations

from terrarium.engine import SeededRNG, Simulation
from terrarium.world import Grid, WorldState


def test_simulation_step_increments_tick_by_one() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    rng = SeededRNG(999)
    sim = Simulation(world, rng)

    assert sim.world.tick == 0
    sim.step()
    assert sim.world.tick == 1


def test_simulation_run_increments_tick_by_n_steps() -> None:
    world = WorldState(Grid(3, 3), seed=1)
    rng = SeededRNG(123)
    sim = Simulation(world, rng)

    sim.run(10)
    assert sim.world.tick == 10


def test_simulation_is_deterministic_for_tick_sequence() -> None:
    world1 = WorldState(Grid(3, 3), seed=1)
    world2 = WorldState(Grid(3, 3), seed=1)

    rng1 = SeededRNG(42)
    rng2 = SeededRNG(42)

    sim1 = Simulation(world1, rng1)
    sim2 = Simulation(world2, rng2)

    seq1: list[int] = []
    seq2: list[int] = []

    for _ in range(5):
        sim1.step()
        sim2.step()
        seq1.append(sim1.world.tick)
        seq2.append(sim2.world.tick)

    assert seq1 == seq2


def test_simulation_exposes_world_and_rng() -> None:
    world = WorldState(Grid(2, 2), seed=5)
    rng = SeededRNG(6)
    sim = Simulation(world, rng)

    assert sim.world is world
    assert sim.rng is rng
