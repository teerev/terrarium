from terrarium.entities.organism import create_organism
from terrarium.world.grid import Position


def test_initial_organism_lineage_defaults() -> None:
    org = create_organism(Position(1, 2), energy=10, birth_tick=7)

    assert org.parent_id is None
    assert org.generation == 0
    assert org.lineage_id == org.id
    assert org.birth_tick == 7


def test_offspring_inherits_lineage_and_increments_generation_and_sets_parent() -> None:
    parent = create_organism(Position(0, 0), energy=10, birth_tick=3)

    child = create_organism(
        Position(0, 1),
        energy=5,
        parent_id=parent.id,
        lineage_id=parent.lineage_id,
        generation=parent.generation + 1,
        birth_tick=4,
    )

    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == 4
