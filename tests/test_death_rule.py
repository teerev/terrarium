from __future__ import annotations

from terrarium.engine.rules.death import DeathRule
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_death_rule_removes_organisms_with_zero_energy_and_updates_indices() -> None:
    world = WorldState(Grid(3, 3), seed=1)

    alive = Organism(position=Position(0, 0), energy=1, id="alive")  # type: ignore[arg-type]
    dead0 = Organism(position=Position(1, 1), energy=0, id="dead0")  # type: ignore[arg-type]

    world.add_entity(alive)
    world.add_entity(dead0)

    removed = DeathRule().apply(world)

    assert [str(eid) for eid in removed] == ["dead0"]

    assert world.get_entity("dead0") is None  # type: ignore[arg-type]
    assert world.get_entities_at(Position(1, 1)) == []

    assert world.get_entity("alive") is not None  # type: ignore[arg-type]
    assert len(world.get_entities_at(Position(0, 0))) == 1


def test_death_rule_removal_is_deterministic_by_id() -> None:
    world = WorldState(Grid(3, 3), seed=1)

    # Insert in reverse order; removal should be sorted by id.
    d2 = Organism(position=Position(0, 0), energy=0, id="b")  # type: ignore[arg-type]
    d1 = Organism(position=Position(0, 1), energy=0, id="a")  # type: ignore[arg-type]

    world.add_entity(d2)
    world.add_entity(d1)

    removed = DeathRule().apply(world)
    assert [str(eid) for eid in removed] == ["a", "b"]

    assert world.get_entity("a") is None  # type: ignore[arg-type]
    assert world.get_entity("b") is None  # type: ignore[arg-type]
