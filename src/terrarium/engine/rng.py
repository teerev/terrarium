from __future__ import annotations

"""Random number generation utilities.

Provides a default RNG implementation that satisfies the core RandomSource
protocol.
"""

import random

from terrarium.core.protocols import RandomSource


class DefaultRandom(RandomSource):
    """Default RNG wrapper around Python's standard library RNG."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def random(self) -> float:
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)
