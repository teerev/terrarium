from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.consumption import ConsumptionRule
from terrarium.engine.rules.death import DeathRule
from terrarium.engine.rules.energy import EnergyRule
from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.engine.rules.spawning import ResourceSpawner
from terrarium.engine.simulation import Simulation
from terrarium.events.emitter import EventEmitter
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState


@dataclass(slots=True)
class Simulator:
    """Convenience wrapper around :class:`terrarium.engine.simulation.Simulation`."""

    world: WorldState
    rng: SeededRNG
    simulation: Simulation

    @classmethod
    def create(
        cls,
        *,
        seed: int = 1,
        width: int = 10,
        height: int = 10,
        profiler: object | None = None,
    ) -> "Simulator":
        world = WorldState(Grid(width, height), seed=int(seed))
        rng = world.rng
        return cls(world, rng, cls._build_simulation(world, rng, profiler=profiler))

    @classmethod
    def _build_simulation(cls, world: WorldState, rng: SeededRNG, *, profiler: object | None = None) -> Simulation:
        emitter = EventEmitter()

        sim = Simulation(
            world,
            rng,
            resource_spawner=ResourceSpawner(),
            movement_rule=MovementRule(),
            energy_rule=EnergyRule(metabolism_rate=0),
            death_rule=DeathRule(),
            event_emitter=emitter,
            profiler=profiler,
        )

        # Rules currently implemented elsewhere; kept to preserve wiring points.
        _ = ConsumptionRule  # noqa: F841
        _ = ReproductionRule  # noqa: F841

        return sim

    def __init__(self, world: WorldState, rng: SeededRNG, *, profiler: object | None = None) -> None:
        self.world = world
        self.rng = rng
        self.simulation = self._build_simulation(world, rng, profiler=profiler)

    def step(self) -> None:
        self.simulation.step()

    def run(self, n_steps: int) -> None:
        self.simulation.run(n_steps)
