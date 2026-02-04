from __future__ import annotations

import pytest

from terrarium.entities import DEFAULT_GENOME, Genome


def test_genome_immutable() -> None:
    g = DEFAULT_GENOME
    with pytest.raises(Exception):
        # frozen dataclass should prevent mutation
        g.speed = 0.9  # type: ignore[misc]


def test_genome_hashable_and_equality() -> None:
    g1 = Genome(speed=0.5, sense_range=3.0, metabolism=1.0, reproduction_threshold=20)
    g2 = Genome(speed=0.5, sense_range=3.0, metabolism=1.0, reproduction_threshold=20)
    assert g1 == g2
    d = {g1: "ok"}
    assert d[g2] == "ok"


def test_genome_serialization_roundtrip() -> None:
    g1 = DEFAULT_GENOME
    payload = g1.to_dict()
    g2 = Genome.from_dict(payload)
    assert g2 == g1
    assert g2.to_dict() == payload


def test_default_genome_values() -> None:
    g = DEFAULT_GENOME
    assert isinstance(g.speed, (int, float))
    assert isinstance(g.sense_range, (int, float))
    assert isinstance(g.metabolism, (int, float))
    assert isinstance(g.reproduction_threshold, (int, float))
    assert g.speed > 0
    assert g.sense_range > 0
    assert g.metabolism > 0
    assert g.reproduction_threshold > 0
