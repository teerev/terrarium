from __future__ import annotations

from typing import Any

import pytest

from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.entities.organism import Organism, create_organism
from terrarium.entities.resource import Resource
from terrarium.world import Grid, WorldState
from terrarium.world.grid import Position


def snapshot_world_state(world: WorldState) -> dict[str, Any]:
    entities: list[object] = list(world.iter_entities())

    organisms: list[Organism] = [e for e in entities if isinstance(e, Organism)]
    resources: list[Resource] = [e for e in entities if isinstance(e, Resource)]

    organisms_snap = [
        {
            "id": str(o.id),
            "x": o.position.x,
            "y": o.position.y,
            "energy": o.energy,
            "age": o.age,
        }
        for o in sorted(organisms, key=lambda o: str(o.id))
    ]

    resources_snap = [
        {
            "id": str(r.id),
            "x": r.position.x,
            "y": r.position.y,
            "energy_value": r.energy_value,
            "consumed": r.consumed,
        }
        for r in sorted(resources, key=lambda r: str(r.id))
    ]

    return {
        "tick": world.tick,
        "seed": world.seed,
        "grid": {"width": world.grid.width, "height": world.grid.height},
        "organisms": organisms_snap,
        "resources": resources_snap,
    }


def _run(seed: int, steps: int) -> dict[str, Any]:
    grid = Grid(width=6, height=6)
    world = WorldState(grid=grid, seed=seed)
    rng = SeededRNG(seed)

    # Seeded initial organisms (ids derived from rng) to ensure full determinism.
    for _ in range(4):
        pos = Position(x=rng.randint(0, grid.width - 1), y=rng.randint(0, grid.height - 1))
        energy = rng.randint(3, 9)
        world.add_entity(create_organism(position=pos, energy=energy, rng=rng))

    spawner = ResourceSpawner(spawn_rate=1.0, max_resources=50, energy_range=(1, 5))
    sim = Simulation(world=world, rng=rng, spawner=spawner)
    sim.run(steps)
    return snapshot_world_state(world)


@pytest.mark.parametrize("seed", [0, 1, 42])
@pytest.mark.parametrize("steps", [1, 10])
def test_same_seed_produces_identical_world_state(seed: int, steps: int) -> None:
    s1 = _run(seed=seed, steps=steps)
    s2 = _run(seed=seed, steps=steps)

    assert s1["tick"] == steps
    assert s2["tick"] == steps

    # Deep equality: includes positions, energy, resource spawns, and IDs.
    assert s1 == s2


def test_different_seeds_differ() -> None:
    s1 = _run(seed=7, steps=10)
    s2 = _run(seed=8, steps=10)

    # At least one of these should differ with overwhelming likelihood given spawn_rate=1.0.
    assert (s1["organisms"] != s2["organisms"]) or (s1["resources"] != s2["resources"])
    # And the snapshots should not be identical overall.
    assert s1 != s2
