"""Simulation coordination types.

This module defines a minimal Simulation placeholder responsible for holding
references to the world and random source.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.world.state import WorldState


@dataclass(slots=True)
class Simulation:
    """A simulation instance.

    Placeholder: will later implement stepping, scheduling, and system updates.
    """

    world: WorldState
    rng: RandomSource

    def step(self) -> None:
        """Advance the simulation by one tick (placeholder)."""

        return None
