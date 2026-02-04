from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.simulation import Simulation
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_movement_to_neighbor_or_stay_and_world_index_updated() -> None:
    grid = Grid(width=3, height=3)
    world = WorldState(grid=grid, seed=123)

    org = create_organism(position=Position(1, 1), energy=10)
    world.add_entity(org)

    sim = Simulation(world=world, rng=SeededRNG(1))

    old_pos = org.position
    sim.step()
    new_pos = org.position

    # World index should no longer contain organism at old position.
    assert org not in world.get_entities_at(old_pos)
    # World index should contain organism at new position.
    assert org in world.get_entities_at(new_pos)

    # New position is either a neighbor or the same (stay).
    neighbors = set(grid.neighbors(old_pos))
    assert new_pos == old_pos or new_pos in neighbors


def test_movement_wraps_grid() -> None:
    grid = Grid(width=2, height=2)
    world = WorldState(grid=grid, seed=0)

    org = create_organism(position=Position(0, 0), energy=10)
    world.add_entity(org)

    sim = Simulation(world=world, rng=SeededRNG(5))
    old = org.position
    sim.step()
    new = org.position

    # Must always be wrapped inside bounds.
    assert 0 <= new.x < grid.width
    assert 0 <= new.y < grid.height

    # Must be neighbor-or-stay in wrapped space.
    assert new == old or new in set(grid.neighbors(old))


def test_movement_deterministic_same_seed() -> None:
    grid = Grid(width=5, height=5)

    def run(seed: int) -> list[Position]:
        world = WorldState(grid=grid, seed=0)
        org = create_organism(position=Position(2, 2), energy=10)
        world.add_entity(org)
        sim = Simulation(world=world, rng=SeededRNG(seed))

        positions = [org.position]
        for _ in range(5):
            sim.step()
            positions.append(org.position)
        return positions

    assert run(42) == run(42)
