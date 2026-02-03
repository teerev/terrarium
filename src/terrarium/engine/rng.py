"""terrarium.engine.rng

Deterministic random number generation for the simulation.

This module defines :class:`~terrarium.engine.rng.SeededRNG`, a small wrapper
around Python's :class:`random.Random` that:

- Produces reproducible sequences given the same seed.
- Provides a single, injectable RNG object for all simulation randomness.
- Supports snapshotting/restoring RNG state for save/load.

Design notes
------------
- This module is the only place in the package that imports :mod:`random`.
  All other modules should receive a RNG instance (dependency injection)
  instead of calling module-level randomness functions.
- The wrapper exposes a minimal surface area required by the simulation.
- The underlying state returned by :meth:`get_state` is the CPython
  ``random.Random`` internal state tuple and is intended to be treated as an
  opaque, serializable value.
"""

from __future__ import annotations

import random
from typing import Any, MutableSequence, Sequence, Tuple

# Public alias for serialized RNG state. Kept simple and intentionally opaque.
Rng = Tuple[Any, ...]


class SeededRNG:
    """A deterministic RNG wrapper backed by ``random.Random``.

    Parameters
    ----------
    seed:
        The initial seed used to initialize the underlying generator.

    Notes
    -----
    - The original seed is stored and can be retrieved via the :attr:`seed`
      property to support snapshot metadata and debugging.
    - To checkpoint an in-progress simulation, use :meth:`get_state` and later
      restore with :meth:`set_state`.
    """

    def __init__(self, seed: int):
        self._seed = int(seed)
        self._rng = random.Random(self._seed)

    @property
    def seed(self) -> int:
        """Return the original seed used to initialize this RNG."""

        return self._seed

    def random(self) -> float:
        """Return the next random float in the range ``[0.0, 1.0)``."""

        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Return a random integer ``N`` such that ``a <= N <= b``."""

        return self._rng.randint(a, b)

    def choice(self, seq: Sequence[Any]) -> Any:
        """Return a random element from *seq*.

        This matches the behavior of :meth:`random.Random.choice` and will
        raise ``IndexError`` for an empty sequence.
        """

        return self._rng.choice(seq)

    def shuffle(self, seq: MutableSequence[Any]) -> None:
        """Shuffle *seq* in-place.

        This operates in-place like :func:`random.shuffle`.
        """

        self._rng.shuffle(seq)

    def gauss(self, mu: float, sigma: float) -> float:
        """Return a random float drawn from a Gaussian distribution."""

        return self._rng.gauss(mu, sigma)

    def get_state(self) -> Rng:
        """Return the internal generator state.

        The returned value is an opaque tuple suitable for serialization.
        It can be restored later with :meth:`set_state`.
        """

        state = self._rng.getstate()
        # random.Random.getstate returns a tuple; we expose it as our Rng alias.
        return state  # type: ignore[return-value]

    def set_state(self, state: Rng) -> None:
        """Restore the internal generator state.

        Parameters
        ----------
        state:
            A value previously produced by :meth:`get_state`.
        """

        self._rng.setstate(state)

    def fork(self, seed: int | None = None) -> "SeededRNG":
        """Create a child RNG.

        This is a convenience for future use. If *seed* is not provided, the
        child seed is generated from this RNG deterministically.
        """

        if seed is None:
            # Use full 32-bit range for reproducibility across runs.
            seed = self._rng.randint(0, 2**32 - 1)
        return SeededRNG(int(seed))
