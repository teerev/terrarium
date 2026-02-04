from __future__ import annotations

from terrarium.engine.rng import SeededRNG


def test_seeded_rng_reproducible_and_state_checkpoint() -> None:
    r1 = SeededRNG(42)
    seq1 = [r1.random(), r1.randint(1, 10), r1.gauss(0.0, 1.0)]

    r2 = SeededRNG(42)
    seq2 = [r2.random(), r2.randint(1, 10), r2.gauss(0.0, 1.0)]

    assert seq1 == seq2

    r3 = SeededRNG(123)
    s = r3.get_state()
    a1 = [r3.random(), r3.randint(1, 10)]

    r4 = SeededRNG(999)
    r4.set_state(s)
    a2 = [r4.random(), r4.randint(1, 10)]

    assert a1 == a2
