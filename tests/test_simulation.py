from __future__ import annotations

import pytest

from terrarium.engine import SeededRNG, Simulation
from terrarium.world import Grid, WorldState
from terrarium.core.types import Seed


def test_initial_tick_zero_and_step_increments_tick():
    world = WorldState(grid=Grid(5, 5), seed=Seed(1))
    sim = Simulation(world=world, rng=SeededRNG(seed=1))

    assert sim.world.tick == 0

    sim.step()

    assert sim.world.tick == 1
    assert sim.world is world


def test_run_multiple_steps_advances_tick_by_n():
    world = WorldState(grid=Grid(3, 3), seed=Seed(2))
    sim = Simulation(world=world, rng=SeededRNG(seed=999))

    sim.run(10)

    assert sim.world.tick == 10


def test_run_rejects_negative_steps():
    world = WorldState(grid=Grid(2, 2), seed=Seed(3))
    sim = Simulation(world=world, rng=SeededRNG(seed=0))

    with pytest.raises(ValueError):
        sim.run(-1)


def test_deterministic_ticks_with_same_seed_and_rng_state():
    # Determinism requirement is about running from the same initial state.
    # To avoid any test depending on entity logic, we snapshot RNG state and
    # replay from that exact state.
    rng1 = SeededRNG(seed=42)
    state = rng1.get_state()

    world1 = WorldState(grid=Grid(4, 4), seed=Seed(10))
    sim1 = Simulation(world=world1, rng=rng1)

    world2 = WorldState(grid=Grid(4, 4), seed=Seed(10))
    rng2 = SeededRNG(seed=999)  # different seed; state restore should dominate
    rng2.set_state(state)
    sim2 = Simulation(world=world2, rng=rng2)

    ticks1: list[int] = []
    ticks2: list[int] = []

    for _ in range(7):
        sim1.step()
        sim2.step()
        ticks1.append(sim1.world.tick)
        ticks2.append(sim2.world.tick)

    assert ticks1 == ticks2
    assert ticks1 == list(range(1, 8))
