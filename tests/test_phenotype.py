from __future__ import annotations

from terrarium.entities.genome import Genome
from terrarium.entities.phenotype import Phenotype


def test_from_genome_is_deterministic() -> None:
    g = Genome(speed=0.25, sense_range=4, metabolism=0.5, reproduction_threshold=7)
    p1 = Phenotype.from_genome(g)
    p2 = Phenotype.from_genome(g)
    assert p1 == p2


def test_traits_are_in_operational_ranges() -> None:
    # extreme-ish values to exercise clamping
    g = Genome(speed=999.0, sense_range=999, metabolism=-10.0, reproduction_threshold=999)
    p = Phenotype.from_genome(g)

    assert 0.5 <= p.speed <= 2.5
    assert 1 <= p.sense_range <= 21
    assert 1 <= p.metabolism_rate <= 5
    assert 10 <= p.reproduction_threshold <= 110


def test_default_genome_maps_to_expected_values() -> None:
    p = Phenotype.from_genome(Genome())
    assert p.speed == 1.5
    assert p.sense_range == 7
    assert p.metabolism_rate == 1
    assert p.reproduction_threshold == 30
