from __future__ import annotations

"""Core timestep simulation loop.

This module intentionally contains only the skeleton needed to advance the world
state by discrete ticks in a deterministic, well-defined order.

Notes
-----
- The RNG is provided from the outside and is not created internally.
- Entity update logic is out of scope; placeholder phase hooks exist for future
  behavior.
"""

from terrarium.core.protocols import RandomSource
from terrarium.world.state import WorldState


class Simulation:
    """Main simulation runner.

    Parameters
    ----------
    world:
        The world state to advance.
    rng:
        Random source used for any stochastic behavior. Must be provided by the
        caller to preserve determinism and testability.
    """

    def __init__(self, world: WorldState, rng: RandomSource) -> None:
        self.world = world
        self.rng = rng

    def step(self) -> None:
        """Advance the simulation by exactly one tick."""

        # Phase order is intentionally fixed and explicit.
        self._phase_move()
        self._phase_consume()
        self._phase_reproduce()
        self._phase_cleanup()

        # Commit the timestep.
        self.world.step_tick()

    def run(self, n_steps: int) -> None:
        """Run the simulation for n_steps ticks."""

        if n_steps < 0:
            raise ValueError("n_steps must be non-negative")

        for _ in range(n_steps):
            self.step()

    # --- Placeholder phase hooks (out of scope for now) ---

    def _phase_move(self) -> None:
        return None

    def _phase_consume(self) -> None:
        return None

    def _phase_reproduce(self) -> None:
        return None

    def _phase_cleanup(self) -> None:
        return None
