from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_creates_offspring_inherits_genome_and_lineage_and_splits_energy() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    rng = SeededRNG(123)

    # Use normalized gene value 0.0 to ensure phenotype threshold is the minimum
    # per the work order (even if the current phenotype mapping differs, energy=60
    # exceeds all expected thresholds).
    genome = Genome(reproduction_threshold=0.0)  # type: ignore[arg-type]

    parent = Organism(
        position=Position(2, 3),
        energy=60,
        id=world.rng.randint(0, 2**32 - 1).to_bytes(4, "big").hex(),  # type: ignore[arg-type]
        genome=genome,
        birth_tick=world.tick,
    )
    world.add_entity(parent)

    rule = ReproductionRule()
    babies = rule.apply(world, rng)

    assert len(babies) == 1
    child = babies[0]

    assert child.position == parent.position
    assert child.genome == parent.genome

    # Energy split: child gets floor(60/2)=30, parent keeps 30.
    assert child.energy == 30
    assert parent.energy == 30

    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == world.tick


def test_reproduction_is_deterministic_by_parent_id_order_and_all_can_reproduce_same_tick() -> None:
    world = WorldState(Grid(5, 5), seed=2)
    rng = SeededRNG(999)

    # Energy high enough to exceed any threshold.
    a = Organism(position=Position(1, 1), energy=50, id="a")
    b = Organism(position=Position(1, 1), energy=50, id="b")
    world.add_entity(b)
    world.add_entity(a)

    babies = ReproductionRule().apply(world, rng)

    assert len(babies) == 2

    # Parents both split energy.
    assert a.energy == 25
    assert b.energy == 25

    # Deterministic order: offspring correspond to parents in sorted id order.
    assert babies[0].parent_id == "a"
    assert babies[1].parent_id == "b"
