from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.engine.simulation import Simulation
from terrarium.entities.resource import Resource
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState


def _resource_positions(world: WorldState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for e in world.iter_entities():
        if isinstance(e, Resource):
            out.append((e.position.x, e.position.y))
    return out


def _resource_energies(world: WorldState) -> list[int]:
    out: list[int] = []
    for e in world.iter_entities():
        if isinstance(e, Resource):
            out.append(e.energy_value)
    return out


def test_spawner_respects_max() -> None:
    world = WorldState(Grid(4, 4), seed=1)
    rng = SeededRNG(1)
    spawner = ResourceSpawner(spawn_rate=1.0, max_resources=2, energy_range=(1, 3))

    sim = Simulation(world=world, rng=rng, spawner=spawner)
    sim.run(10)

    assert len(_resource_positions(world)) == 2


def test_spawner_deterministic_same_seed() -> None:
    def run(seed: int) -> tuple[list[tuple[int, int]], list[int]]:
        world = WorldState(Grid(6, 6), seed=seed)
        rng = SeededRNG(seed)
        spawner = ResourceSpawner(spawn_rate=0.6, max_resources=10, energy_range=(2, 5))
        sim = Simulation(world=world, rng=rng, spawner=spawner)
        sim.run(20)
        return _resource_positions(world), _resource_energies(world)

    p1, e1 = run(42)
    p2, e2 = run(42)

    assert p1 == p2
    assert e1 == e2


def test_spawner_energy_in_range() -> None:
    world = WorldState(Grid(5, 5), seed=7)
    rng = SeededRNG(7)
    spawner = ResourceSpawner(spawn_rate=1.0, max_resources=5, energy_range=(3, 9))

    sim = Simulation(world=world, rng=rng, spawner=spawner)
    sim.run(5)

    energies = _resource_energies(world)
    assert len(energies) == 5
    assert all(3 <= v <= 9 for v in energies)
