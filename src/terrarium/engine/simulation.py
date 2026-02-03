"""Simulation timestep loop.

This module defines :class:`~terrarium.engine.simulation.Simulation`, the core
runner responsible for advancing the world state by discrete timesteps.

Design constraints
------------------
- Fixed timestep: each ``step()`` advances exactly one tick.
- Deterministic: same initial world + same RNG state => same results.
- RNG is injected and passed through; it is never created internally.
- Order of operations within a step is well-defined via phase hooks.

Entity/system logic is intentionally left as placeholder hooks.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.world.state import WorldState


@dataclass(slots=True)
class Simulation:
    """A simulation instance coordinating world state updates."""

    world: WorldState
    rng: RandomSource

    def step(self) -> None:
        """Advance the simulation by exactly one tick.

        Phase order (skeleton):
        1) pre_step
        2) movement
        3) consumption
        4) reproduction
        5) cleanup
        6) tick increment
        7) post_step

        Notes
        -----
        - The tick is incremented exactly once per call.
        - Placeholder phases are provided for future systems.
        """

        self._phase_pre_step()
        self._phase_movement()
        self._phase_consumption()
        self._phase_reproduction()
        self._phase_cleanup()

        # Fixed-timestep: increment exactly once per step.
        self.world.step_tick()

        self._phase_post_step()

    def run(self, n_steps: int) -> None:
        """Run the simulation for ``n_steps`` steps."""

        if n_steps < 0:
            raise ValueError("n_steps must be non-negative")

        for _ in range(n_steps):
            self.step()

    # --- Phase hooks (placeholders) ---
    def _phase_pre_step(self) -> None:
        return None

    def _phase_movement(self) -> None:
        return None

    def _phase_consumption(self) -> None:
        return None

    def _phase_reproduction(self) -> None:
        return None

    def _phase_cleanup(self) -> None:
        return None

    def _phase_post_step(self) -> None:
        return None
