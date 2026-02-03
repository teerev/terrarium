from __future__ import annotations

import pytest

from terrarium.entities.genome import DEFAULT_GENOME, Genome


def test_genome_default_to_dict_roundtrip() -> None:
    d = DEFAULT_GENOME.to_dict()
    g2 = Genome.from_dict(d)
    assert g2 == DEFAULT_GENOME


def test_genome_immutable() -> None:
    g = Genome()
    with pytest.raises(Exception):
        # frozen dataclass should not allow assignment
        g.speed = 0.9  # type: ignore[misc]


def test_genome_hashable_and_comparable() -> None:
    g1 = Genome()
    g2 = Genome()
    assert g1 == g2
    assert hash(g1) == hash(g2)
    d = {g1: "ok"}
    assert d[g2] == "ok"
