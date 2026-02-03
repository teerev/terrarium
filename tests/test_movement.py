from __future__ import annotations

from terrarium.core.types import Seed
from terrarium.engine import SeededRNG, Simulation
from terrarium.engine.rules import MovementRule
from terrarium.entities import create_organism
from terrarium.world import Grid, Position, WorldState


def test_movement_to_neighbor_and_index_updated():
    world = WorldState(grid=Grid(3, 3), seed=Seed(1))
    org = create_organism(Position(1, 1), energy=1)
    world.add_entity(org)

    rule = MovementRule(include_stay=False, adjacency=4)
    sim = Simulation(world=world, rng=SeededRNG(seed=123), movement_rule=rule)

    old = Position(org.position.x, org.position.y)
    sim.step()
    new = org.position

    assert new != old
    assert new in world.grid.neighbors(old, adjacency=4)

    assert org in world.get_entities_at(new)
    assert org not in world.get_entities_at(old)


def test_movement_wraps_grid_and_is_deterministic():
    rule = MovementRule(include_stay=False, adjacency=4)

    def run(seed: int) -> Position:
        world = WorldState(grid=Grid(3, 3), seed=Seed(1))
        org = create_organism(Position(0, 0), energy=1)
        world.add_entity(org)
        sim = Simulation(world=world, rng=SeededRNG(seed=seed), movement_rule=rule)
        sim.step()
        return org.position

    p1 = run(999)
    p2 = run(999)
    p3 = run(1000)

    assert p1 == p2
    assert p1 in {Position(1, 0), Position(2, 0), Position(0, 1), Position(0, 2)}
    assert p3 in {Position(1, 0), Position(2, 0), Position(0, 1), Position(0, 2)}
