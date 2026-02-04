"""Core simulation loop.

This module defines :class:`Simulation`, the minimal runner responsible for
advancing a :class:`terrarium.world.state.WorldState` forward in fixed discrete
timesteps.

Entity update logic, event emission, and pause/resume are intentionally out of
scope for this skeleton.
"""

from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


class Simulation:
    """Main simulation runner.

    The simulation is deterministic as long as callers provide deterministic
    inputs (initial world state + RNG seed/state) and route all randomness
    through the provided RNG.

    Parameters
    ----------
    world:
        The world state container to advance.
    rng:
        Random number generator to use; must be provided by the caller.
    resource_spawner:
        Optional rule component that spawns new Resource entities.
    movement_rule:
        Optional rule component that moves Organism entities.
    energy_rule:
        Optional rule component that drains organism energy each tick.
    """

    def __init__(
        self,
        world: WorldState,
        rng: SeededRNG,
        resource_spawner: ResourceSpawner | None = None,
        movement_rule: MovementRule | None = None,
        energy_rule: EnergyRule | None = None,
    ):
        self.world = world
        self.rng = rng
        self.resource_spawner = resource_spawner
        self.movement_rule = movement_rule
        self.energy_rule = energy_rule

    def step(self) -> None:
        """Advance the simulation by exactly one tick."""

        # Phase order is explicitly defined to keep future behavior stable.
        self._phase_spawn()
        self._phase_move()
        self._phase_energy()
        self._phase_consume()
        self._phase_reproduce()
        self._phase_cleanup()

        # Tick increments exactly once per step.
        self.world.step()

    def run(self, n_steps: int) -> None:
        """Run the simulation for *n_steps* discrete ticks."""

        n = int(n_steps)
        if n < 0:
            raise ValueError("n_steps must be non-negative")
        for _ in range(n):
            self.step()

    # --- Placeholder phase hooks (no-op for now) ---

    def _phase_spawn(self) -> None:
        if self.resource_spawner is None:
            return
        self.resource_spawner.spawn(self.world, self.rng)

    def _phase_move(self) -> None:
        if self.movement_rule is None:
            return

        # WorldState doesn't currently expose an organism iterator; keep changes
        # localized and deterministic by sorting by id string.
        entities = getattr(self.world, "_entities", {})
        organisms: list[Organism] = [e for e in entities.values() if isinstance(e, Organism)]
        organisms.sort(key=lambda o: str(o.id))

        self.movement_rule.apply(organisms, self.world, self.rng)

    def _phase_energy(self) -> None:
        if self.energy_rule is None:
            return

        entities = getattr(self.world, "_entities", {})
        organisms: list[Organism] = [e for e in entities.values() if isinstance(e, Organism)]
        organisms.sort(key=lambda o: str(o.id))

        self.energy_rule.apply(organisms, self.world)

    def _phase_consume(self) -> None:
        return

    def _phase_reproduce(self) -> None:
        return

    def _phase_cleanup(self) -> None:
        return
