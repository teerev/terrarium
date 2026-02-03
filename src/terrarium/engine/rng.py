"""Deterministic RNG wrapper for Terrarium.

This module centralizes all simulation randomness behind a single, injectable
random number generator.

Design goals:
- Reproducible sequences given the same seed.
- No reliance on the global `random` module state.
- Serializable state for snapshot/save-load via get_state()/set_state().

Notes:
- The `random` module is imported only in this file (per project constraint).
- This class is a thin wrapper around `random.Random`.
"""

from __future__ import annotations

from typing import Any, MutableSequence, Sequence

import random


class SeededRNG:
    """A deterministic RNG wrapper around :class:`random.Random`.

    Parameters
    ----------
    seed:
        The initial seed used to initialize the underlying PRNG. The original
        seed value is stored and exposed via the :attr:`seed` property for
        snapshot/serialization metadata.

    The underlying PRNG state can be checkpointed using :meth:`get_state` and
    restored using :meth:`set_state`.
    """

    def __init__(self, seed: int) -> None:
        self._seed = seed
        self._rng = random.Random(seed)

    @property
    def seed(self) -> int:
        """Return the original seed used to initialize this RNG."""

        return self._seed

    def random(self) -> float:
        """Return the next random floating point number in the range [0.0, 1.0)."""

        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""

        return self._rng.randint(a, b)

    def choice(self, seq: Sequence[Any]) -> Any:
        """Choose a random element from a non-empty sequence."""

        return self._rng.choice(seq)

    def shuffle(self, seq: MutableSequence[Any]) -> None:
        """Shuffle a mutable sequence in place."""

        self._rng.shuffle(seq)

    def gauss(self, mu: float, sigma: float) -> float:
        """Return a random number drawn from a Gaussian distribution."""

        return self._rng.gauss(mu, sigma)

    def get_state(self) -> tuple[Any, ...]:
        """Return the internal state of the underlying PRNG.

        The returned state is suitable for serialization and can be supplied to
        :meth:`set_state` to restore the PRNG to the exact same point.
        """

        state = self._rng.getstate()
        # random.Random.getstate() returns a tuple; we normalize the annotation.
        return state  # type: ignore[return-value]

    def set_state(self, state: tuple[Any, ...]) -> None:
        """Restore the internal state of the underlying PRNG."""

        self._rng.setstate(state)  # type: ignore[arg-type]

    def fork(self, seed: int | None = None) -> "SeededRNG":
        """Create a child RNG.

        This is intended for future use (e.g., component-local RNGs) while still
        allowing deterministic behavior.

        Parameters
        ----------
        seed:
            If provided, use this seed for the child. If not provided, derive a
            seed deterministically from this RNG.
        """

        child_seed = seed if seed is not None else self.randint(0, 2**31 - 1)
        return SeededRNG(seed=child_seed)
