from __future__ import annotations

"""Protocol definitions for core interfaces.

Protocols are used so components can depend on behavior (interfaces) rather than
concrete implementations.
"""

from typing import Protocol


class RandomSource(Protocol):
    """Abstract random number generator interface.

    The engine uses this protocol so RNG implementations can be swapped (e.g.,
    deterministic testing vs. production randomness).
    """

    def random(self) -> float:
        """Return the next random float in the range [0.0, 1.0)."""

    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""
