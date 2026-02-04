from __future__ import annotations

from terrarium.engine import SeededRNG


def test_same_seed_same_sequence() -> None:
    rng1 = SeededRNG(seed=42)
    rng2 = SeededRNG(seed=42)

    seq1 = [rng1.random(), rng1.randint(1, 10), rng1.gauss(0.0, 1.0)]
    seq2 = [rng2.random(), rng2.randint(1, 10), rng2.gauss(0.0, 1.0)]

    assert seq1 == seq2
    assert rng1.seed == rng2.seed == 42


def test_state_checkpoint() -> None:
    rng = SeededRNG(seed=123)

    before = [rng.random(), rng.randint(1, 100)]
    state = rng.get_state()

    after1 = [rng.random(), rng.randint(1, 100), rng.gauss(10.0, 2.0)]

    rng.set_state(state)
    after2 = [rng.random(), rng.randint(1, 100), rng.gauss(10.0, 2.0)]

    assert before != after1
    assert after1 == after2
