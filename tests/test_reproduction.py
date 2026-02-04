from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_threshold_position_genome_energy_and_lineage() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    rng = SeededRNG(123)

    # Phenotype reproduction_threshold is derived from genome value via phenotype mapping.
    # Use 0.0 so threshold is at the low end (see phenotype mapping implementation).
    genome = Genome(speed=0.0, sense_range=0.0, metabolism=0.0, reproduction_threshold=0.0)

    parent = create_organism(position=Position(2, 3), energy=11, rng=rng, genome=genome)
    world.add_entity(parent)

    rule = ReproductionRule(offspring_energy_fraction=0.5)

    # Below / equal threshold should not reproduce.
    parent.energy = parent.phenotype.reproduction_threshold
    offspring = rule.apply(world, rng)
    assert offspring == []

    # Above threshold should reproduce.
    parent.energy = parent.phenotype.reproduction_threshold + 2
    offspring = rule.apply(world, rng)
    assert len(offspring) == 1

    child = offspring[0]
    assert child.position == parent.position
    assert child.genome == parent.genome

    # Energy split: child gets int(parent_energy * 0.5) based on energy at reproduction time.
    # parent_energy at reproduction time is threshold+2.
    expected_child_energy = int((parent.phenotype.reproduction_threshold + 2) * 0.5)
    assert child.energy == expected_child_energy
    assert parent.energy == (parent.phenotype.reproduction_threshold + 2) - expected_child_energy

    # Lineage
    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == world.tick


def test_reproduction_deterministic_order_allows_multiple_parents() -> None:
    world = WorldState(Grid(3, 3), seed=999)
    rng = SeededRNG(999)

    genome = Genome(speed=0.0, sense_range=0.0, metabolism=0.0, reproduction_threshold=0.0)

    # Create two organisms with deterministic IDs from the seeded RNG.
    # Add to world in reverse order to ensure deterministic processing is by ID sorting, not insertion.
    b = create_organism(position=Position(1, 1), energy=20, rng=rng, genome=genome)
    a = create_organism(position=Position(0, 0), energy=20, rng=rng, genome=genome)

    world.add_entity(b)
    world.add_entity(a)

    rule = ReproductionRule(offspring_energy_fraction=0.5)
    offspring = rule.apply(world, rng)

    assert len(offspring) == 2

    # Offspring are returned in deterministic order by parent ID order.
    parents_sorted = sorted([a, b], key=lambda o: str(o.id))
    assert offspring[0].parent_id == parents_sorted[0].id
    assert offspring[1].parent_id == parents_sorted[1].id
