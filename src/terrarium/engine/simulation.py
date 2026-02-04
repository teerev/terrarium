from __future__ import annotations

"""Simulation engine placeholder.

This module defines the top-level object responsible for advancing the world
state over time.
"""

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.engine.rng import DefaultRandom
from terrarium.world.state import WorldState


@dataclass(slots=True)
class SimulationEngine:
    """Coordinates advancing a WorldState.

    This placeholder stores references to world state and an RNG. The step logic
    will be implemented in later milestones.
    """

    world: WorldState
    rng: RandomSource

    @classmethod
    def create(cls, world: WorldState, *, seed: int | None = None) -> "SimulationEngine":
        """Create an engine with a default RNG."""

        return cls(world=world, rng=DefaultRandom(seed=seed))

    def step(self) -> None:
        """Advance the simulation by one tick.

        Placeholder: intentionally does not mutate state yet.
        """

        return None
