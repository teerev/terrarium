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
from terrarium.engine.rules.death import DeathRule
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.entities.organism import Organism
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
    spawner:
        Optional resource spawning rule.
    """

    def __init__(
        self,
        world: WorldState,
        rng: RandomSource,
        spawner: ResourceSpawner | None = None,
        movement: MovementRule | None = None,
        energy: EnergyRule | None = None,
        death: DeathRule | None = None,
        reproduction: ReproductionRule | None = None,
    ) -> None:
        self.world = world
        self.rng = rng
        self.spawner = spawner
        self.movement = movement or MovementRule()
        self.energy = energy or EnergyRule()
        self.death = death or DeathRule()
        self.reproduction = reproduction or ReproductionRule()

    def step(self) -> None:
        """Advance the simulation by exactly one tick."""

        # Phase order is intentionally fixed and explicit.
        self._phase_move()
        self._phase_energy()
        self._phase_death()
        self._phase_consume()
        self._phase_reproduce()
        self._phase_cleanup()

        if self.spawner is not None:
            self.spawner.spawn(self.world, self.rng)

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
        organisms = [e for e in self.world.iter_entities() if isinstance(e, Organism)]
        self.movement.apply(organisms, self.world, self.rng)
        return None

    def _phase_energy(self) -> None:
        organisms = [e for e in self.world.iter_entities() if isinstance(e, Organism)]
        self.energy.apply(organisms, self.world)
        return None

    def _phase_death(self) -> None:
        self.death.apply(self.world)
        return None

    def _phase_consume(self) -> None:
        return None

    def _phase_reproduce(self) -> None:
        self.reproduction.apply(self.world, self.rng)
        return None

    def _phase_cleanup(self) -> None:
        return None
