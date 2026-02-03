from __future__ import annotations

from terrarium.engine import SeededRNG, Simulation
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState


def test_step_increments_tick() -> None:
    world = WorldState(Grid(width=3, height=3), seed=123)
    sim = Simulation(world=world, rng=SeededRNG(1))

    assert world.tick == 0
    sim.step()
    assert world.tick == 1


def test_run_multiple_steps_increments_tick_by_n() -> None:
    world = WorldState(Grid(width=3, height=3), seed=123)
    sim = Simulation(world=world, rng=SeededRNG(1))

    sim.run(10)
    assert world.tick == 10


def test_deterministic_ticks_same_seed_and_initial_state() -> None:
    world1 = WorldState(Grid(width=2, height=2), seed=999)
    world2 = WorldState(Grid(width=2, height=2), seed=999)

    rng1 = SeededRNG(42)
    rng2 = SeededRNG(42)

    sim1 = Simulation(world=world1, rng=rng1)
    sim2 = Simulation(world=world2, rng=rng2)

    ticks1 = []
    ticks2 = []
    for _ in range(5):
        sim1.step()
        sim2.step()
        ticks1.append(sim1.world.tick)
        ticks2.append(sim2.world.tick)

    assert ticks1 == [1, 2, 3, 4, 5]
    assert ticks1 == ticks2
