from __future__ import annotations

import pytest

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import Organism
from terrarium.testing import snapshot_world_state
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def _run(seed: int, steps: int) -> WorldState:
    grid = Grid(width=5, height=5)
    world = WorldState(grid, seed=seed)

    # Ensure initial ids are deterministic across runs by using the simulation RNG.
    rng = SeededRNG(seed)

    # Add a couple of organisms with deterministic ids.
    world.add_entity(Organism(position=Position(1, 1), energy=10, rng=rng))
    world.add_entity(Organism(position=Position(3, 2), energy=7, rng=rng))

    sim = Simulation(
        world,
        rng,
        movement_rule=MovementRule(diagonal=False, allow_stay=True),
        energy_rule=EnergyRule(metabolism_rate=1),
        resource_spawner=ResourceSpawner(spawn_rate=1.0, max_resources=50, energy_range=(1, 3)),
    )
    sim.run(steps)
    return world


@pytest.mark.parametrize("seed", [0, 1, 12345])
@pytest.mark.parametrize("steps", [0, 1, 5, 10])
def test_same_seed_produces_identical_final_world_state(seed: int, steps: int) -> None:
    w1 = _run(seed, steps)
    w2 = _run(seed, steps)

    s1 = snapshot_world_state(w1)
    s2 = snapshot_world_state(w2)

    assert s1 == s2


@pytest.mark.parametrize("seed", [2, 99])
def test_positions_energy_and_resource_spawns_match(seed: int) -> None:
    steps = 8
    w1 = _run(seed, steps)
    w2 = _run(seed, steps)

    s1 = snapshot_world_state(w1)
    s2 = snapshot_world_state(w2)

    assert s1["tick"] == s2["tick"] == steps

    # Entity positions match (covers organisms + resources).
    pos1 = [(e["id"], e["position"]) for e in s1["entities"]]
    pos2 = [(e["id"], e["position"]) for e in s2["entities"]]
    assert pos1 == pos2

    # Organism energies match.
    org_energy1 = [(e["id"], e.get("energy")) for e in s1["entities"] if "energy" in e]
    org_energy2 = [(e["id"], e.get("energy")) for e in s2["entities"] if "energy" in e]
    assert org_energy1 == org_energy2

    # Resource spawning positions and values match.
    res1 = [
        (e["id"], e["position"], e.get("energy_value"), e.get("consumed"))
        for e in s1["entities"]
        if "energy_value" in e
    ]
    res2 = [
        (e["id"], e["position"], e.get("energy_value"), e.get("consumed"))
        for e in s2["entities"]
        if "energy_value" in e
    ]
    assert res1 == res2
