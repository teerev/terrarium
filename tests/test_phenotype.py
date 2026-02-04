from __future__ import annotations

from terrarium.entities.genome import Genome
from terrarium.entities.phenotype import Phenotype


def test_phenotype_from_genome_is_deterministic_and_in_ranges() -> None:
    g = Genome(speed=0.5, sense_range=2.0, metabolism=0.1, reproduction_threshold=10)

    p1 = Phenotype.from_genome(g)
    p2 = Phenotype.from_genome(g)

    assert p1 == p2

    assert 0.1 <= p1.speed <= 3.0
    assert 1 <= p1.sense_range <= 10
    assert 1 <= p1.metabolism_rate <= 10
    assert 5 <= p1.reproduction_threshold <= 200
