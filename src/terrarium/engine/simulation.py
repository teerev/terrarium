from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.death import DeathRule
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.entities.organism import Organism
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
        movement_rule: MovementRule | None = None,
        energy_rule: EnergyRule | None = None,
        death_rule: DeathRule | None = None,
    ) -> None:
        self.world = world
        self.rng = rng
        self.resource_spawner = resource_spawner
        self.movement_rule = movement_rule
        self.energy_rule = energy_rule
        self.death_rule = death_rule

    def step(self) -> None:
        """Advance the simulation by exactly one tick."""

        # Phase order is intentionally explicit and stable.
        self._phase_move()
        self._phase_energy()
        self._phase_death()
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

    # --- Placeholder phase hooks ---

    def _phase_move(self) -> None:
        if self.movement_rule is None:
            return

        # Minimal integration: move all Organism instances currently in the world.
        organisms: list[Organism] = []
        for ent in self.world._entities.values():  # type: ignore[attr-defined]
            if isinstance(ent, Organism):
                organisms.append(ent)

        self.movement_rule.apply(organisms, self.world, self.rng)

    def _phase_energy(self) -> None:
        if self.energy_rule is None:
            return

        organisms: list[Organism] = []
        for ent in self.world._entities.values():  # type: ignore[attr-defined]
            if isinstance(ent, Organism):
                organisms.append(ent)

        self.energy_rule.apply(organisms, self.world)

    def _phase_death(self) -> None:
        if self.death_rule is None:
            return

        self.death_rule.apply(self.world)

    def _phase_consume(self) -> None:
        return

    def _phase_reproduce(self) -> None:
        return

    def _phase_cleanup(self) -> None:
        return
