from __future__ import annotations

from terrarium.analysis import LineageTree
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_public_import_lineage_tree() -> None:
    # Public API import path should work.
    from terrarium.analysis.lineage import LineageTree as Direct

    assert LineageTree is Direct


def test_worldstate_auto_records_births() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    lt = LineageTree()
    world.lineage_tree = lt

    parent = Organism(position=Position(1, 1), energy=10, birth_tick=world.tick)
    world.add_entity(parent)

    child = Organism(
        position=Position(2, 2),
        energy=5,
        parent_id=parent.id,
        lineage_id=parent.lineage_id,
        generation=parent.generation + 1,
        birth_tick=world.tick,
        genome=parent.genome,
    )
    world.add_entity(child)

    assert lt.get_children(parent.id) == [child.id]
    assert lt.get_ancestors(child.id) == [parent.id]
    assert set(lt.get_descendants(parent.id)) == {child.id}

    parent_rec = lt.get_organism_record(parent.id)
    child_rec = lt.get_organism_record(child.id)

    assert parent_rec.birth_tick == world.tick
    assert child_rec.parent_id == parent.id
    assert child_rec.generation == parent.generation + 1
