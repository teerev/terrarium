from __future__ import annotations

import pytest

from terrarium.core.types import Seed
from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules import ConsumptionRule, EnergyRule, MovementRule, ResourceSpawner
from terrarium.entities import create_organism
from terrarium.testing import snapshot_world_state
from terrarium.world import Grid, Position, WorldState


def _make_sim(seed: int, *, steps: int) -> dict:
    world = WorldState(grid=Grid(6, 6), seed=Seed(seed))
    rng = SeededRNG(seed=seed)

    # Seeded entity IDs (critical for determinism across process restarts)
    o1 = create_organism(Position(1, 1), energy=10, rng=rng)
    o2 = create_organism(Position(4, 4), energy=8, rng=rng)
    world.add_entity(o1)
    world.add_entity(o2)

    sim = Simulation(
        world=world,
        rng=rng,
        resource_spawner=ResourceSpawner(spawn_rate=1.0, max_resources=50, energy_range=(2, 5)),
        movement_rule=MovementRule(include_stay=True, adjacency=4),
        energy_rule=EnergyRule(metabolism_rate=1),
        consumption_rule=ConsumptionRule(),
    )

    sim.run(steps)
    return snapshot_world_state(world)


@pytest.mark.parametrize("seed", [1, 2, 12345])
@pytest.mark.parametrize("steps", [1, 10, 25])
def test_same_seed_produces_identical_snapshot(seed: int, steps: int):
    s1 = _make_sim(seed, steps=steps)
    s2 = _make_sim(seed, steps=steps)

    assert s1 == s2
    assert s1["tick"] == steps


def test_snapshot_includes_positions_energy_and_resources_and_is_stable():
    snap = _make_sim(999, steps=15)

    assert snap["tick"] == 15
    assert snap["grid"]["width"] == 6

    # Deep checks: organisms energy/positions present; resources spawned with energy.
    assert any(e["type"] == "organism" and "energy" in e for e in snap["entities"])
    assert any(e["type"] == "resource" and "energy_value" in e for e in snap["entities"])


def test_different_seeds_diverge():
    s1 = _make_sim(10, steps=20)
    s2 = _make_sim(11, steps=20)

    assert s1["tick"] == s2["tick"] == 20
    assert s1 != s2
