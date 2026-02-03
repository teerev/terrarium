from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.io.snapshot import WorldSnapshot, create_snapshot, restore_snapshot
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_snapshot_roundtrip_smoke() -> None:
    grid = Grid(5, 4)
    world = WorldState(grid, seed=123)
    rng = SeededRNG(123)

    org = Organism(
        position=Position(1, 2),
        energy=7,
        id="org-1",
        genome=Genome(speed=0.25, sense_range=2, metabolism=0.5, reproduction_threshold=9),
        parent_id=None,
        lineage_id="org-1",
        generation=0,
        birth_tick=0,
    )
    org.tick()
    org.tick()

    res = Resource(position=Position(3, 1), energy_value=5, id="res-1", consumed=True)

    world.add_entity(org)
    world.add_entity(res)
    world.step()

    snap = create_snapshot(world, rng)
    payload = snap.to_dict()
    # Ensure JSON-serializable structure (no tuples).
    assert isinstance(payload["rng"]["state"], list)

    world2, rng2 = restore_snapshot(WorldSnapshot.from_dict(payload))

    assert world2.tick == world.tick
    assert (world2.grid.width, world2.grid.height) == (world.grid.width, world.grid.height)
    assert rng2.seed == rng.seed
    assert rng2.get_state() == rng.get_state()

    o2 = world2.get_entity("org-1")
    assert isinstance(o2, Organism)
    assert (o2.position.x, o2.position.y) == (1, 2)
    assert o2.energy == 7
    assert o2.age == 2
    assert o2.parent_id is None
    assert o2.lineage_id == "org-1"
    assert o2.generation == 0
    assert o2.birth_tick == 0
    assert o2.genome.to_dict() == org.genome.to_dict()

    r2 = world2.get_entity("res-1")
    assert isinstance(r2, Resource)
    assert (r2.position.x, r2.position.y) == (3, 1)
    assert r2.energy_value == 5
    assert r2.consumed is True
