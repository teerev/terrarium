from __future__ import annotations

from terrarium.analysis.species import SpeciesClassifier, cluster_by_genome, genome_distance
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.world.grid import Position


def test_genome_distance_euclidean() -> None:
    g1 = Genome(speed=0.0, sense_range=0, metabolism=0.0, reproduction_threshold=0)
    g2 = Genome(speed=3.0, sense_range=4, metabolism=0.0, reproduction_threshold=0)
    # sqrt(3^2 + 4^2) = 5
    assert genome_distance(g1, g2) == 5.0


def test_species_classifier_groups_similar_and_counts_population() -> None:
    clf = SpeciesClassifier(threshold=0.3)

    g_a = Genome(speed=0.5, sense_range=3, metabolism=0.1, reproduction_threshold=10)
    g_a2 = Genome(speed=0.55, sense_range=3, metabolism=0.1, reproduction_threshold=10)
    g_b = Genome(speed=0.9, sense_range=9, metabolism=0.9, reproduction_threshold=40)

    o1 = Organism(Position(0, 0), 1, genome=g_a)
    o2 = Organism(Position(0, 0), 1, genome=g_a2)
    o3 = Organism(Position(0, 0), 1, genome=g_b)

    s1 = clf.classify(o1)
    s2 = clf.classify(o2)
    s3 = clf.classify(o3)

    assert s1 == s2
    assert s3 != s1
    assert clf.get_population(s1) == 2
    assert clf.get_population(s3) == 1
    assert clf.species_count == 2


def test_cluster_by_genome_is_deterministic_for_order() -> None:
    g1 = Genome(speed=0.5, sense_range=3, metabolism=0.1, reproduction_threshold=10)
    g2 = Genome(speed=0.52, sense_range=3, metabolism=0.1, reproduction_threshold=10)
    g3 = Genome(speed=0.95, sense_range=9, metabolism=0.9, reproduction_threshold=45)

    o1 = Organism(Position(0, 0), 1, genome=g1)
    o2 = Organism(Position(0, 0), 1, genome=g2)
    o3 = Organism(Position(0, 0), 1, genome=g3)

    c1 = cluster_by_genome([o1, o2, o3], threshold=0.3)
    c2 = cluster_by_genome([o1, o2, o3], threshold=0.3)

    assert set(c1.keys()) == set(c2.keys())
    assert [len(c1[k]) for k in sorted(c1.keys())] == [len(c2[k]) for k in sorted(c2.keys())]
