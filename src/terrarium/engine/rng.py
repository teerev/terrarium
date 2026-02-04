"""Random number generation utilities for the engine.

This module defines a minimal RNG wrapper that satisfies the core RandomSource
protocol.
"""

from __future__ import annotations

import random


class DefaultRNG:
    """Default RNG implementation used by the engine.

    This is a thin wrapper around :class:`random.Random`.
    """

    def __init__(self, seed: int | None = None) -> None:
        self._random = random.Random(seed)

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""

        return self._random.randint(a, b)
