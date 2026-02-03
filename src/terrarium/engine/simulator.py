"""Simulation loop placeholder.

This module defines a minimal Simulator façade that will later coordinate
updates across the world and entities.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import Rng
from terrarium.world.state import WorldState


@dataclass(slots=True)
class Simulator:
    """A placeholder simulation runner."""

    world: WorldState
    rng: Rng

    def step(self) -> None:
        """Advance the simulation by one tick.

        No logic is implemented yet.
        """

        return None
