from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.mutation import MutationConfig, mutate_genome
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_mutate_genome_deterministic_same_seed() -> None:
    g = Genome(speed=0.5, sense_range=5, metabolism=0.5, reproduction_threshold=10)

    rng1 = SeededRNG(123)
    rng2 = SeededRNG(123)

    out1 = mutate_genome(g, rng1, rate=1.0, magnitude=0.2)
    out2 = mutate_genome(g, rng2, rate=1.0, magnitude=0.2)

    assert out1 == out2


def test_mutate_genome_rate_zero_returns_identical() -> None:
    g = Genome(speed=0.5, sense_range=5, metabolism=0.5, reproduction_threshold=10)
    rng = SeededRNG(1)

    out = mutate_genome(g, rng, rate=0.0, magnitude=10.0)
    assert out == g


def test_mutate_genome_clamps_to_valid_ranges() -> None:
    # Start at extremes and use huge magnitude so we likely go out of range.
    g = Genome(speed=1.0, sense_range=10, metabolism=0.0, reproduction_threshold=50)
    rng = SeededRNG(999)

    out = mutate_genome(g, rng, rate=1.0, magnitude=1000.0)

    assert 0.0 <= out.speed <= 1.0
    assert 0 <= out.sense_range <= 10
    assert 0.0 <= out.metabolism <= 1.0
    assert 0 <= out.reproduction_threshold <= 50


def test_reproduction_rule_applies_mutation_to_offspring_genome() -> None:
    world = WorldState(Grid(5, 5), seed=0)
    rng = world.rng

    parent = Organism(
        position=Position(0, 0),
        energy=1000,
        rng=rng,
        genome=Genome(speed=0.5, sense_range=3, metabolism=0.1, reproduction_threshold=10),
    )
    world.add_entity(parent)

    rule = ReproductionRule(mutation=MutationConfig(rate=1.0, magnitude=0.5))
    offspring = rule.apply(world, rng)

    assert len(offspring) == 1
    assert offspring[0].genome != parent.genome
