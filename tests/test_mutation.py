from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.mutation import mutate_genome
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_mutation_deterministic_and_in_range() -> None:
    g = Genome(speed=0.5, sense_range=0.5, metabolism=0.5, reproduction_threshold=50)

    rng1 = SeededRNG(123)
    rng2 = SeededRNG(123)

    m1 = mutate_genome(g, rng1, rate=1.0, magnitude=0.25)
    m2 = mutate_genome(g, rng2, rate=1.0, magnitude=0.25)

    assert m1 == m2

    d = m1.to_dict()
    assert 0.0 <= float(d["speed"]) <= 1.0
    assert 0.0 <= float(d["sense_range"]) <= 1.0
    assert 0.0 <= float(d["metabolism"]) <= 1.0
    assert 0 <= float(d["reproduction_threshold"]) <= 100.0


def test_reproduction_includes_mutation() -> None:
    grid = Grid(5, 5)
    world = WorldState(grid=grid, seed=0)
    rng = SeededRNG(999)

    parent_genome = Genome(speed=0.5, sense_range=0.5, metabolism=0.5, reproduction_threshold=0)
    parent = create_organism(position=Position(1, 1), energy=100, rng=rng, genome=parent_genome)
    world.add_entity(parent)

    rule = ReproductionRule(offspring_energy_fraction=0.5, mutation_rate=1.0, mutation_magnitude=0.2)
    kids = rule.apply(world, rng)

    assert len(kids) == 1
    assert kids[0].genome != parent.genome
