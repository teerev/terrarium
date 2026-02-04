"""Deterministic random number generator utilities for the simulation engine.

This module is the *only* place in the Terrarium codebase that should import
Python's :mod:`random` module.

The simulation must route all randomness through :class:`SeededRNG` (or another
object implementing the same interface) to guarantee deterministic, reproducible
runs given the same seed, and to enable snapshot/save-load functionality via
serializable RNG state.
"""

from __future__ import annotations

import random
from typing import Any, MutableSequence, Sequence


class SeededRNG:
    """A deterministic RNG wrapper built on :class:`random.Random`.

    The wrapper:
    - guarantees reproducible random sequences when created with the same seed
    - exposes a small, stable API for simulation components
    - supports checkpointing via :meth:`get_state` / :meth:`set_state`

    Notes
    -----
    - This is not intended for cryptographic use.
    - This class wraps an *instance* of :class:`random.Random` and never uses the
      global module-level functions.
    """

    def __init__(self, seed: int):
        """Create a new seeded RNG.

        Parameters
        ----------
        seed:
            Seed used to initialize the underlying PRNG. The seed is stored and
            can be retrieved later via the :pyattr:`seed` property.
        """

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
        """Return a random element from *seq*.

        Parameters
        ----------
        seq:
            A non-empty sequence to choose from.
        """

        return self._rng.choice(seq)

    def shuffle(self, seq: MutableSequence[Any]) -> None:
        """Shuffle *seq* in place."""

        self._rng.shuffle(seq)

    def gauss(self, mu: float, sigma: float) -> float:
        """Return a random value sampled from a Gaussian distribution."""

        return self._rng.gauss(mu, sigma)

    def get_state(self) -> tuple[Any, ...]:
        """Return the internal PRNG state.

        The returned value is intended to be serializable by callers (e.g., via
        pickle/JSON with custom handling) for save/load functionality.
        """

        state = self._rng.getstate()
        # random.Random.getstate() returns a tuple; we keep the signature stable
        # and explicit as a tuple[Any, ...] for snapshotting.
        return state  # type: ignore[return-value]

    def set_state(self, state: tuple[Any, ...]) -> None:
        """Restore the internal PRNG state.

        Parameters
        ----------
        state:
            A state previously produced by :meth:`get_state`.
        """

        self._rng.setstate(state)  # type: ignore[arg-type]

    def fork(self, seed: int | None = None) -> "SeededRNG":
        """Create a new child RNG.

        This is provided for future use (e.g., component-local RNGs) while
        keeping determinism explicit.

        If *seed* is None, a deterministic seed is generated from this RNG.
        """

        if seed is None:
            seed = self.randint(0, 2**31 - 1)
        return SeededRNG(int(seed))


# Backwards-compatible alias for the engine's default RNG.
DefaultRNG = SeededRNG
