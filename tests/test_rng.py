from __future__ import annotations

from terrarium.engine import SeededRNG


def test_same_seed_same_sequence() -> None:
    rng1 = SeededRNG(seed=42)
    rng2 = SeededRNG(seed=42)

    seq1 = [rng1.random(), rng1.randint(1, 10), rng1.gauss(0.0, 1.0)]
    seq2 = [rng2.random(), rng2.randint(1, 10), rng2.gauss(0.0, 1.0)]

    assert seq1 == seq2
    assert rng1.seed == rng2.seed == 42


def test_state_checkpoint_restore() -> None:
    rng = SeededRNG(seed=123)

    _ = rng.random()
    checkpoint = rng.get_state()

    a1 = rng.randint(1, 100)
    b1 = rng.choice(["a", "b", "c", "d"])

    rng.set_state(checkpoint)
    a2 = rng.randint(1, 100)
    b2 = rng.choice(["a", "b", "c", "d"])

    assert a1 == a2
    assert b1 == b2


def test_shuffle_deterministic() -> None:
    r1 = SeededRNG(seed=7)
    r2 = SeededRNG(seed=7)

    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1, 2, 3, 4, 5, 6]

    r1.shuffle(l1)
    r2.shuffle(l2)

    assert l1 == l2
    assert l1 != [1, 2, 3, 4, 5, 6]
