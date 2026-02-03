"""Random number generation.

This module provides a minimal RNG abstraction to allow deterministic
simulation runs by injecting a seeded generator.
"""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(slots=True)
class Rng:
    """A minimal random number generator wrapper."""

    seed: int | None = None

    def __post_init__(self) -> None:
        self._random = random.Random(self.seed)

    def random(self) -> float:
        """Return the next random float in the range [0.0, 1.0)."""

        return self._random.random()
