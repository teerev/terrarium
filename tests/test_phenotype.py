from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.entities.phenotype import Phenotype


def test_phenotype_from_genome() -> None:
    g = Genome(speed=0.0, sense_range=0.0, metabolism=0.0, reproduction_threshold=0.0)
    p = Phenotype.from_genome(g)

    assert isinstance(p.speed, float)
    assert isinstance(p.sense_range, int)
    assert isinstance(p.metabolism_rate, int)
    assert isinstance(p.reproduction_threshold, int)


def test_phenotype_deterministic() -> None:
    g = Genome(speed=0.2, sense_range=0.3, metabolism=0.4, reproduction_threshold=2.0)

    p1 = Phenotype.from_genome(g)
    p2 = Phenotype.from_genome(g)

    assert p1 == p2
    assert p1.speed == p2.speed


def test_phenotype_traits_in_operational_ranges() -> None:
    # Include negative genes to ensure clamping produces usable values.
    g = Genome(speed=-10.0, sense_range=-1.0, metabolism=-5.0, reproduction_threshold=-2.0)
    p = Phenotype.from_genome(g)

    assert p.speed >= 0.5
    assert p.sense_range >= 1
    assert p.metabolism_rate >= 1
    assert p.reproduction_threshold >= 1


def test_different_genomes_different_phenotypes() -> None:
    g1 = Genome(speed=0.1, sense_range=0.1, metabolism=0.1, reproduction_threshold=1.0)
    g2 = Genome(speed=0.9, sense_range=0.1, metabolism=0.1, reproduction_threshold=1.0)

    p1 = Phenotype.from_genome(g1)
    p2 = Phenotype.from_genome(g2)

    assert p1.speed != p2.speed
    assert p1 != p2


def test_organism_has_phenotype_via_genome() -> None:
    g = Genome(speed=0.7, sense_range=0.2, metabolism=0.3, reproduction_threshold=4.0)
    org = Organism(position=(0, 0), energy=10, genome=g)

    assert org.phenotype == Phenotype.from_genome(g)
    assert org.phenotype.speed > 0
