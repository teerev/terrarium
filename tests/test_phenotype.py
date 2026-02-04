from __future__ import annotations

from terrarium.entities import DEFAULT_GENOME, Genome, Phenotype, create_organism
from terrarium.world.grid import Position


def test_phenotype_from_genome_and_deterministic() -> None:
    p1 = Phenotype.from_genome(DEFAULT_GENOME)
    p2 = Phenotype.from_genome(DEFAULT_GENOME)

    assert p1 == p2
    assert p1.speed > 0


def test_phenotype_traits_in_range_and_organism_access() -> None:
    g = Genome(speed=0.0, sense_range=1.0, metabolism=0.5, reproduction_threshold=100)
    p = Phenotype.from_genome(g)

    assert 0.5 <= p.speed <= 2.0
    assert 1 <= p.sense_range <= 10
    assert 1 <= p.metabolism_rate <= 5
    assert 10 <= p.reproduction_threshold <= 50

    o = create_organism(Position(0, 0), 10, genome=g)
    assert o.phenotype == p
