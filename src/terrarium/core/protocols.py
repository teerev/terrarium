"""Protocol definitions for terrarium.

Protocols define interfaces between subpackages without forcing concrete
implementations or introducing import cycles.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .types import Coordinate, Seed


@runtime_checkable
class HasPosition(Protocol):
    """Something that has a position in world space."""

    @property
    def position(self) -> Coordinate:
        """Current position in world coordinates."""


class RandomSource(Protocol):
    """Abstract random number generator used by the simulation.

    This allows the engine to accept different RNG implementations while keeping
    APIs testable and deterministic.
    """

    def seed(self, value: Seed) -> None:
        """Seed the generator for deterministic output."""

    def random(self) -> float:
        """Return the next random float in the half-open interval [0.0, 1.0)."""
