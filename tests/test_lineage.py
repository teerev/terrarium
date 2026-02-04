from __future__ import annotations

from terrarium.entities import create_organism
from terrarium.world import Position


def test_initial_organism_lineage() -> None:
    org = create_organism(Position(0, 0), 10, birth_tick=7)

    assert org.parent_id is None
    assert org.generation == 0
    assert org.lineage_id == org.id
    assert org.birth_tick == 7


def test_offspring_inherits_lineage_id_and_increments_generation() -> None:
    parent = create_organism(Position(1, 1), 10, birth_tick=3)
    child = create_organism(
        Position(2, 2),
        5,
        parent_id=parent.id,
        lineage_id=parent.lineage_id,
        generation=parent.generation + 1,
        birth_tick=4,
    )

    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == 4
