from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.world.state import WorldState


class Simulation:
    """Core simulation loop.

    Design constraints:
    - Fixed timestep: each :meth:`step` advances exactly one tick.
    - Deterministic: callers must inject the RNG; Simulation will not create one.

    Entity logic is intentionally out of scope for now; phase hooks are provided
    as placeholders for future extension.
    """

    def __init__(self, world: WorldState, rng: SeededRNG) -> None:
        self.world = world
        self.rng = rng

    def step(self) -> None:
        """Advance the simulation by one tick."""

        # Well-defined order of operations (placeholders for now).
        self._phase_move()
        self._phase_consume()
        self._phase_reproduce()
        self._phase_cleanup()

        # Fixed timestep tick advancement.
        self.world.step()

    def run(self, n_steps: int) -> None:
        """Advance the simulation by multiple ticks."""

        if n_steps < 0:
            raise ValueError("n_steps must be >= 0")
        for _ in range(n_steps):
            self.step()

    # --- Phase hooks (no-op for now) ---
    def _phase_move(self) -> None:
        return

    def _phase_consume(self) -> None:
        return

    def _phase_reproduce(self) -> None:
        return

    def _phase_cleanup(self) -> None:
        return
