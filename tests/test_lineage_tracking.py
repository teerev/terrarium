from __future__ import annotations

from terrarium.entities.organism import Organism, create_organism
from terrarium.world.grid import Position


def test_initial_organism_defaults() -> None:
    o = Organism(position=Position(0, 0), energy=5)
    assert o.parent_id is None
    assert o.generation == 0
    assert o.lineage_id == o.id
    assert o.birth_tick == 0


def test_offspring_inherits_lineage() -> None:
    parent = Organism(position=Position(1, 2), energy=10)
    child = create_organism(
        position=Position(2, 2),
        energy=3,
        parent_id=parent.id,
        lineage_id=parent.lineage_id,
        generation=parent.generation + 1,
        birth_tick=7,
    )

    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == 7
