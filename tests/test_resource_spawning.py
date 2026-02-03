from __future__ import annotations

from terrarium.core.types import Seed
from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules import ResourceSpawner
from terrarium.entities import EntityType
from terrarium.world import Grid, WorldState


def _resource_positions_and_energy(world: WorldState) -> list[tuple[int, int, int]]:
    out: list[tuple[int, int, int]] = []
    for e in world.iter_entities():
        if getattr(e, "entity_type", None) is EntityType.RESOURCE:
            out.append((e.position.x, e.position.y, int(getattr(e, "energy_value"))))
    # stable ordering for deterministic comparisons
    return sorted(out)


def test_spawner_respects_max_and_creates_resources():
    world = WorldState(grid=Grid(4, 4), seed=Seed(1))
    rng = SeededRNG(seed=123)

    spawner = ResourceSpawner(spawn_rate=10.0, max_resources=2, energy_range=(1, 3))
    sim = Simulation(world=world, rng=rng, resource_spawner=spawner)

    sim.step()
    assert len(_resource_positions_and_energy(world)) == 2

    # Further steps should not exceed max_resources
    sim.step()
    assert len(_resource_positions_and_energy(world)) == 2


def test_spawner_deterministic_same_seed_same_sequence_and_energy_in_range():
    spawner = ResourceSpawner(spawn_rate=1.0, max_resources=10, energy_range=(5, 7))

    world1 = WorldState(grid=Grid(5, 5), seed=Seed(1))
    world2 = WorldState(grid=Grid(5, 5), seed=Seed(1))

    sim1 = Simulation(world=world1, rng=SeededRNG(seed=999), resource_spawner=spawner)
    sim2 = Simulation(world=world2, rng=SeededRNG(seed=999), resource_spawner=spawner)

    for _ in range(5):
        sim1.step()
        sim2.step()

    seq1 = _resource_positions_and_energy(world1)
    seq2 = _resource_positions_and_energy(world2)

    assert seq1 == seq2
    assert len(seq1) == 5

    for x, y, energy in seq1:
        assert 0 <= x < world1.grid.width
        assert 0 <= y < world1.grid.height
        assert 5 <= energy <= 7
