from __future__ import annotations

import pytest

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import create_organism
from terrarium.testing import snapshot_world_state
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def _run(seed: int, steps: int):
    rng = SeededRNG(seed)
    world = WorldState(grid=Grid(6, 6), seed=seed)

    # Ensure determinism covers entity ids too by deriving them from the same RNG.
    world.add_entity(create_organism(Position(1, 1), energy=10, rng=rng))
    world.add_entity(create_organism(Position(3, 4), energy=7, rng=rng))

    sim = Simulation(
        world=world,
        rng=rng,
        resource_spawner=ResourceSpawner(spawn_rate=1.0, max_resources=10, energy_range=(2, 5)),
        movement_rule=MovementRule(allow_stay=True, diagonals=False),
        energy_rule=EnergyRule(metabolism_rate=1),
    )

    sim.run(steps)
    return snapshot_world_state(world)


@pytest.mark.parametrize("seed", [0, 1, 42, 123456])
@pytest.mark.parametrize("steps", [0, 1, 5, 10])
def test_same_seed_produces_identical_world_state(seed: int, steps: int):
    a = _run(seed, steps)
    b = _run(seed, steps)

    assert a == b

    # Explicit checks requested by the work order (redundant but clearer).
    assert a["tick"] == b["tick"]

    assert [(o["x"], o["y"]) for o in a["organisms"]] == [(o["x"], o["y"]) for o in b["organisms"]]
    assert [o["energy"] for o in a["organisms"]] == [o["energy"] for o in b["organisms"]]

    assert [(r["x"], r["y"], r["energy_value"]) for r in a["resources"]] == [
        (r["x"], r["y"], r["energy_value"]) for r in b["resources"]
    ]
