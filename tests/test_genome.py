from dataclasses import FrozenInstanceError

import pytest

from terrarium.entities import DEFAULT_GENOME, Genome


def test_genome_immutable() -> None:
    g = Genome(speed=0.1, sense_range=0.2, metabolism=0.3, reproduction_threshold=4)
    with pytest.raises(FrozenInstanceError):
        g.speed = 0.9  # type: ignore[misc]


def test_genome_hashable_and_equality() -> None:
    g1 = Genome(speed=0.1, sense_range=0.2, metabolism=0.3, reproduction_threshold=4)
    g2 = Genome(speed=0.1, sense_range=0.2, metabolism=0.3, reproduction_threshold=4)
    g3 = Genome(speed=0.1, sense_range=0.2, metabolism=0.31, reproduction_threshold=4)

    assert g1 == g2
    assert g1 != g3

    d = {g1: "ok"}
    assert d[g2] == "ok"


def test_genome_serialization_roundtrip() -> None:
    g = Genome(speed=0.25, sense_range=1.0, metabolism=0.0, reproduction_threshold=7)
    d = g.to_dict()
    g2 = Genome.from_dict(d)
    assert g2 == g


def test_default_genome_valid() -> None:
    d = DEFAULT_GENOME.to_dict()
    assert d["speed"] > 0
    assert d["reproduction_threshold"] > 0
