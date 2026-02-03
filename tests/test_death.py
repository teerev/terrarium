from __future__ import annotations

from terrarium.engine.rules.death import DeathRule
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_zero_energy_dies_and_updates_world_state_indices() -> None:
    world = WorldState(grid=Grid(width=3, height=3), seed=0)

    organism = create_organism(position=Position(0, 0), energy=0)
    world.add_entity(organism)

    removed = DeathRule().apply(world)

    assert removed == [organism.id]
    assert world.get_entity(organism.id) is None
    assert world.get_entities_at(Position(0, 0)) == []


def test_positive_energy_survives() -> None:
    world = WorldState(grid=Grid(width=3, height=3), seed=0)

    organism = create_organism(position=Position(1, 1), energy=5)
    world.add_entity(organism)

    removed = DeathRule().apply(world)

    assert removed == []
    assert world.get_entity(organism.id) is organism
