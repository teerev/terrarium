from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState


def _snapshot(world: WorldState):
    entities = getattr(world, "_entities")
    items = []
    for e in entities.values():
        items.append((e.position.x, e.position.y, getattr(e, "energy_value", None)))
    return sorted(items)


def test_resource_spawning_deterministic_and_capped():
    grid = Grid(5, 4)

    spawner = ResourceSpawner(spawn_rate=1.0, max_resources=3, energy_range=(2, 4))

    w1 = WorldState(grid=grid, seed=123)
    s1 = SeededRNG(123)
    for _ in range(10):
        spawner.spawn(w1, s1)

    w2 = WorldState(grid=grid, seed=123)
    s2 = SeededRNG(123)
    for _ in range(10):
        spawner.spawn(w2, s2)

    assert _snapshot(w1) == _snapshot(w2)
    assert len(_snapshot(w1)) == 3
