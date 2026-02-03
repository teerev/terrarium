"""Deterministic random number generation for the simulation engine.

Design goals
------------
- Provide a single RNG wrapper used by simulation code to ensure reproducibility.
- Ensure determinism: the same seed produces the same output sequence.
- Support checkpointing via get_state()/set_state() so simulations can be
  snapshotted and later resumed.

Important constraint
--------------------
This is the *only* module in the package that imports the standard library
``random`` module. Other modules should depend on :class:`~terrarium.engine.rng.SeededRNG`
(or interfaces/protocols) and never call ``random.*`` directly.
"""

from __future__ import annotations

import random
from typing import Any, MutableSequence, Sequence

from terrarium.core.protocols import RandomSource
from terrarium.core.types import Seed


class SeededRNG(RandomSource):
    """A deterministic RNG wrapper backed by :class:`random.Random`.

    Parameters
    ----------
    seed:
        Seed used to initialize the RNG. The original seed is stored and can be
        retrieved later via the :pyattr:`seed` property for snapshot/metadata.

    Notes
    -----
    - This class wraps an internal :class:`random.Random` instance (not the
      global module functions).
    - The internal state is serializable via :meth:`get_state`.
    """

    def __init__(self, seed: int | Seed) -> None:
        self._seed: int = int(seed)
        self._rng = random.Random(self._seed)

    @property
    def seed(self) -> int:
        """Return the original seed used to construct this RNG."""

        return self._seed

    def random(self) -> float:
        """Return the next random float in the half-open interval [0.0, 1.0)."""

        return float(self._rng.random())

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that ``a <= N <= b``."""

        return int(self._rng.randint(a, b))

    def choice(self, seq: Sequence[Any]) -> Any:
        """Return a randomly selected element from *seq*.

        Raises
        ------
        IndexError
            If *seq* is empty (matches ``random.Random.choice`` behavior).
        """

        return self._rng.choice(seq)

    def shuffle(self, seq: MutableSequence[Any]) -> None:
        """Shuffle *seq* in place."""

        self._rng.shuffle(seq)

    def gauss(self, mu: float, sigma: float) -> float:
        """Return a random value from a Gaussian distribution."""

        return float(self._rng.gauss(mu, sigma))

    def get_state(self) -> tuple[Any, ...]:
        """Return the internal RNG state for checkpointing.

        The returned value is suitable for serialization (e.g., via pickle/JSON
        transformation) and can be restored with :meth:`set_state`.
        """

        return self._rng.getstate()

    def set_state(self, state: tuple[Any, ...]) -> None:
        """Restore a state previously produced by :meth:`get_state`."""

        self._rng.setstate(state)

    def fork(self, seed: int | Seed) -> "SeededRNG":
        """Create a child RNG.

        This is a convenience for future use when components want their own RNG
        while remaining deterministic and explicit.
        """

        return SeededRNG(seed=seed)


class DefaultRandom(SeededRNG):
    """Backward-compatible alias for the engine's default RNG.

    Historically the engine exported ``DefaultRandom`` as its RNG. The preferred
    API going forward is :class:`SeededRNG`.
    """

    pass
