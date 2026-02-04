from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.resource import Resource, create_resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ResourceSpawner:
    """Rule for spawning new resources into the world.

    Parameters
    ----------
    spawn_rate:
        Probability per tick to attempt a single spawn (0.0 to 1.0).
    max_resources:
        Hard cap on number of resources allowed in the world.
    energy_range:
        Inclusive (min_energy, max_energy) for spawned resource energy.
    """

    spawn_rate: float = 0.0
    max_resources: int = 0
    energy_range: tuple[int, int] = (1, 1)

    def __post_init__(self) -> None:
        if self.spawn_rate < 0.0:
            raise ValueError("spawn_rate must be >= 0.0")
        if self.spawn_rate > 1.0:
            raise ValueError("spawn_rate must be <= 1.0")
        if self.max_resources < 0:
            raise ValueError("max_resources must be >= 0")
        lo, hi = self.energy_range
        if lo <= 0 or hi <= 0:
            raise ValueError("energy_range values must be positive")
        if lo > hi:
            raise ValueError("energy_range min must be <= max")

    def spawn(self, world: WorldState, rng: SeededRNG) -> list[Resource]:
        """Possibly spawn resources and add them to the world.

        Returns a list of newly spawned Resource entities.
        """

        if self.max_resources == 0 or self.spawn_rate <= 0.0:
            return []

        # Enforce cap based on current resource count.
        existing = self._count_resources(world)
        if existing >= self.max_resources:
            return []

        # Probability check for a single spawn attempt per tick.
        if rng.random() >= self.spawn_rate:
            return []

        x = rng.randint(0, world.grid.width - 1)
        y = rng.randint(0, world.grid.height - 1)
        pos = Position(x, y)

        lo, hi = self.energy_range
        energy = rng.randint(lo, hi)

        # Deterministic ID generation via rng.
        resource = create_resource(pos, energy, rng=rng)
        world.add_entity(resource)
        return [resource]

    def _count_resources(self, world: WorldState) -> int:
        # WorldState doesn't expose an entity iterator; access the internal index.
        # This keeps changes minimal and localized to the spawning rule.
        entities = getattr(world, "_entities", {})
        n = 0
        for e in entities.values():
            if isinstance(e, Resource):
                n += 1
        return n
