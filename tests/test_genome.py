from __future__ import annotations

from terrarium.entities.genome import DEFAULT_GENOME, Genome


def test_genome_roundtrip_hashable() -> None:
    g = Genome()
    d = g.to_dict()
    g2 = Genome.from_dict(d)

    assert g == g2
    assert hash(g) == hash(g2)

    # Can be used as a dict key
    m = {g: "ok"}
    assert m[g2] == "ok"

    # Default genome is available and serializable
    assert isinstance(DEFAULT_GENOME.to_dict(), dict)
