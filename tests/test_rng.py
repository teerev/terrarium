from __future__ import annotations

from terrarium.engine.rng import SeededRNG


def test_seeded_rng_same_seed_same_sequence() -> None:
    r1 = SeededRNG(42)
    r2 = SeededRNG(42)

    seq1 = [r1.random() for _ in range(5)] + [r1.randint(1, 10) for _ in range(5)]
    seq2 = [r2.random() for _ in range(5)] + [r2.randint(1, 10) for _ in range(5)]

    assert seq1 == seq2


def test_seed_property_returns_original_seed() -> None:
    r = SeededRNG(123)
    assert r.seed == 123


def test_get_state_set_state_checkpointing() -> None:
    r = SeededRNG(7)

    # Advance a bit, checkpoint, then continue.
    _ = [r.random() for _ in range(3)]
    state = r.get_state()
    after_state = [r.random() for _ in range(5)]

    # Restore and ensure we reproduce the same continuation.
    r.set_state(state)
    after_restore = [r.random() for _ in range(5)]

    assert after_restore == after_state
