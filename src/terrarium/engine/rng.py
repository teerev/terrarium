"""Randomness utilities for the simulation engine.

The engine uses an abstract RandomSource protocol to remain testable.
This module provides a small default implementation.
"""

from __future__ import annotations

import random

from terrarium.core.protocols import RandomSource
from terrarium.core.types import Seed


class DefaultRandom(RandomSource):
    """Default RNG implementation backed by Python's random.Random."""

    def __init__(self, seed: Seed | None = None) -> None:
        self._rng = random.Random()
        if seed is not None:
            self.seed(seed)

    def seed(self, value: Seed) -> None:
        self._rng.seed(int(value))

    def random(self) -> float:
        return float(self._rng.random())
