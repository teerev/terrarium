from __future__ import annotations

"""Deterministic RNG wrapper for the simulation engine.

This module is the *only* place in the engine package that imports Python's
standard library :mod:`random` module.

The simulation should depend on :class:`~terrarium.engine.rng.SeededRNG` (or a
compatible interface such as :class:`terrarium.core.protocols.RandomSource`)
so that all stochastic behavior can be made deterministic and reproducible.

Key properties:
- Same seed -> same sequence across runs.
- State can be checkpointed and restored via get_state/set_state.
- Provides common RNG convenience methods used throughout the simulation.
"""

import random
from typing import Any, MutableSequence, Sequence


class SeededRNG:
    """A deterministic, seedable random number generator.

    This class wraps :class:`random.Random` (an independent RNG instance, not the
    global module-level generator) and records the original seed for later
    retrieval (e.g., snapshot/serialization metadata).

    Parameters
    ----------
    seed:
        Seed value used to initialize the underlying RNG. The same seed will
        produce the same sequence of values.

    Notes
    -----
    - All randomness in the simulation should flow through a single instance of
      this class.
    - Use :meth:`get_state` and :meth:`set_state` to checkpoint and restore the
      RNG stream.
    """

    def __init__(self, seed: int) -> None:
        self._seed = int(seed)
        self._rng = random.Random(self._seed)

    @property
    def seed(self) -> int:
        """Return the original seed used to initialize this RNG."""

        return self._seed

    def random(self) -> float:
        """Return the next random float in the range [0.0, 1.0)."""

        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""

        return self._rng.randint(a, b)

    def choice(self, seq: Sequence[Any]) -> Any:
        """Return a random element from a non-empty sequence."""

        return self._rng.choice(seq)

    def shuffle(self, seq: MutableSequence[Any]) -> None:
        """Shuffle a mutable sequence in-place."""

        self._rng.shuffle(seq)

    def gauss(self, mu: float, sigma: float) -> float:
        """Return a random number sampled from a Gaussian distribution."""

        return self._rng.gauss(mu, sigma)

    def get_state(self) -> tuple[Any, ...]:
        """Return a serialized representation of the RNG's internal state."""

        state = self._rng.getstate()
        # random.Random.getstate() returns an opaque tuple; we normalize to
        # tuple[Any, ...] to keep typing simple.
        return state  # type: ignore[return-value]

    def set_state(self, state: tuple[Any, ...]) -> None:
        """Restore the RNG's internal state from a previously saved state."""

        self._rng.setstate(state)  # type: ignore[arg-type]

    def fork(self, seed: int) -> "SeededRNG":
        """Create a new independent RNG with the provided seed.

        This is a convenience for future use (e.g., per-component RNG streams)
        while still keeping determinism explicit.
        """

        return SeededRNG(seed=seed)


# Backwards-compatibility alias used by existing package exports.
DefaultRandom = SeededRNG
