from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_creates_offspring_and_splits_energy_and_lineage() -> None:
    world = WorldState(grid=Grid(5, 5), seed=123)
    rng = SeededRNG(1)

    # genome.reproduction_threshold is expected normalized; 0.0 -> phenotype threshold near minimum.
    genome = Genome(reproduction_threshold=0.0)

    parent1 = create_organism(Position(2, 2), energy=20, rng=rng, genome=genome)
    parent2 = create_organism(Position(1, 1), energy=21, rng=rng, genome=genome)
    world.add_entity(parent1)
    world.add_entity(parent2)

    rule = ReproductionRule()
    children = rule.apply(world, rng)

    assert len(children) == 2

    # Offspring at parent's position, same genome, correct lineage
    by_parent = {c.parent_id: c for c in children}
    c1 = by_parent[parent1.id]
    c2 = by_parent[parent2.id]

    assert c1.position == parent1.position
    assert c2.position == parent2.position

    assert c1.genome == parent1.genome
    assert c2.genome == parent2.genome

    assert c1.lineage_id == parent1.lineage_id
    assert c2.lineage_id == parent2.lineage_id

    assert c1.generation == parent1.generation + 1
    assert c2.generation == parent2.generation + 1

    assert c1.birth_tick == world.tick
    assert c2.birth_tick == world.tick

    # Energy split: child gets floor(parent_energy_before/2), parent reduced by that amount.
    # parent1: 20 -> child 10, parent 10
    # parent2: 21 -> child 10, parent 11
    assert c1.energy == 10
    assert parent1.energy == 10

    assert c2.energy == 10
    assert parent2.energy == 11
