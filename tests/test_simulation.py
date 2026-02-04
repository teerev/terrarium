from __future__ import annotations

from terrarium.engine import SeededRNG, Simulation
from terrarium.world import Grid, WorldState


def test_initial_tick_zero() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    sim = Simulation(world, SeededRNG(123))

    assert sim.world.tick == 0


def test_exposes_world_and_rng() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    rng = SeededRNG(123)
    sim = Simulation(world, rng)

    assert sim.world is world
    assert sim.rng is rng


def test_step_increments_tick() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    sim = Simulation(world, SeededRNG(123))

    assert world.tick == 0
    sim.step()
    assert world.tick == 1


def test_run_multiple_steps_and_deterministic_ticks() -> None:
    world_a = WorldState(Grid(5, 5), seed=7)
    world_b = WorldState(Grid(5, 5), seed=7)

    sim_a = Simulation(world_a, SeededRNG(7))
    sim_b = Simulation(world_b, SeededRNG(7))

    ticks_a: list[int] = []
    ticks_b: list[int] = []

    for _ in range(10):
        sim_a.step()
        sim_b.step()
        ticks_a.append(world_a.tick)
        ticks_b.append(world_b.tick)

    assert world_a.tick == 10
    assert world_b.tick == 10
    assert ticks_a == ticks_b


def test_run_advances_tick_by_n() -> None:
    world = WorldState(Grid(5, 5), seed=42)
    sim = Simulation(world, SeededRNG(42))

    sim.run(10)
    assert world.tick == 10
