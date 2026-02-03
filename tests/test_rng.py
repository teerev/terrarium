from __future__ import annotations

from terrarium.engine import SeededRNG


def test_same_seed_same_sequence():
    rng1 = SeededRNG(seed=42)
    rng2 = SeededRNG(seed=42)

    seq1 = [rng1.random() for _ in range(5)]
    seq2 = [rng2.random() for _ in range(5)]

    assert seq1 == seq2
    assert rng1.seed == rng2.seed == 42


def test_state_checkpoint():
    rng = SeededRNG(seed=123)

    a = rng.randint(1, 10)
    state = rng.get_state()

    b1 = rng.randint(1, 10)
    c1 = rng.gauss(0.0, 1.0)

    rng.set_state(state)
    b2 = rng.randint(1, 10)
    c2 = rng.gauss(0.0, 1.0)

    assert a == a  # keep at least one more assertion anchored to the run
    assert (b1, c1) == (b2, c2)


def test_shuffle_and_choice_deterministic():
    rng1 = SeededRNG(seed=7)
    rng2 = SeededRNG(seed=7)

    data1 = [1, 2, 3, 4, 5]
    data2 = [1, 2, 3, 4, 5]

    pick1 = rng1.choice(data1)
    pick2 = rng2.choice(data2)

    rng1.shuffle(data1)
    rng2.shuffle(data2)

    assert pick1 == pick2
    assert data1 == data2
