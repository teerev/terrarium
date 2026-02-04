from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.movement import MovementRule
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_movement_deterministic_and_updates_world_index() -> None:
    grid = Grid(3, 3)
    world1 = WorldState(grid=grid, seed=1)
    world2 = WorldState(grid=grid, seed=1)

    org1a = create_organism(Position(0, 0), energy=1)
    org1b = create_organism(Position(0, 0), energy=1, entity_id=org1a.id)

    world1.add_entity(org1a)
    world2.add_entity(org1b)

    rule = MovementRule(allow_stay=False, diagonals=False)
    rng1 = SeededRNG(123)
    rng2 = SeededRNG(123)

    rule.apply([org1a], world1, rng1)
    rule.apply([org1b], world2, rng2)

    assert org1a.position == org1b.position

    # Index moved: old position empty, new position contains organism
    assert world1.get_entities_at(Position(0, 0)) == []
    assert world1.get_entities_at(org1a.position)[0].id == org1a.id


def test_movement_wraps_at_boundaries() -> None:
    grid = Grid(3, 3)
    world = WorldState(grid=grid, seed=1)

    org = create_organism(Position(0, 0), energy=1)
    world.add_entity(org)

    # Force selection of (-1,0) among [(-1,0),(1,0),(0,-1),(0,1)] by choosing index 0.
    class _FixedRNG:
        def choice(self, seq):
            return seq[0]

    rule = MovementRule(allow_stay=False, diagonals=False)
    rule.apply([org], world, _FixedRNG())

    assert org.position == Position(2, 0)
