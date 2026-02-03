from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.world.state import WorldState


class Simulation:
    """Core simulation loop runner.

    This is a minimal fixed-timestep skeleton. Each call to :meth:`step`
    advances the provided world by exactly one tick, in a well-defined phase
    order.

    Notes
    -----
    - RNG must be provided (dependency injection) and is not created internally.
    - Entity update logic is intentionally left as placeholder hooks.
    """

    def __init__(
        self,
        world: WorldState,
        rng: SeededRNG,
        *,
        resource_spawner: ResourceSpawner | None = None,
    ) -> None:
        self.world = world
        self.rng = rng
        self.resource_spawner = resource_spawner

    def step(self) -> None:
        """Advance the simulation by exactly one tick."""

        # Phase order is intentionally explicit and stable.
        self._phase_move()
        self._phase_consume()
        self._phase_reproduce()
        self._phase_cleanup()

        # Spawning rules (post-cleanup, pre-tick-commit).
        if self.resource_spawner is not None:
            self.resource_spawner.spawn(self.world, self.rng)

        # Commit timestep.
        self.world.step()

    def run(self, n_steps: int) -> None:
        """Run the simulation for *n_steps* discrete timesteps."""

        steps = int(n_steps)
        if steps < 0:
            raise ValueError("n_steps must be non-negative")

        for _ in range(steps):
            self.step()

    # --- Placeholder phase hooks (no behavior yet) ---

    def _phase_move(self) -> None:
        return

    def _phase_consume(self) -> None:
        return

    def _phase_reproduce(self) -> None:
        return

    def _phase_cleanup(self) -> None:
        return
