"""Simulation loop placeholder.

This module defines a minimal simulation container that wires together the
world and random source.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.world.state import WorldState


@dataclass(slots=True)
class Simulation:
    """A minimal simulation runner.

    Future implementations may advance time steps, update entities, and apply
    rules. For now it stores references to the world and RNG.
    """

    world: WorldState
    rng: RandomSource

    def step(self) -> None:
        """Advance the simulation by one tick.

        Placeholder: no simulation logic is implemented yet.
        """

        return None
