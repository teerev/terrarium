from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.entities.resource import Resource, create_resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(slots=True)
class ResourceSpawner:
    """Rule for spawning Resource entities into the world.

    Parameters
    ----------
    spawn_rate:
        Probability per tick of spawning a single resource.
    max_resources:
        Maximum number of resources allowed in the world.
    energy_range:
        Inclusive (min_energy, max_energy) range for resource energy_value.
    """

    spawn_rate: float = 0.0
    max_resources: int = 0
    energy_range: tuple[int, int] = (1, 1)

    def __post_init__(self) -> None:
        if self.spawn_rate < 0.0:
            raise ValueError("spawn_rate must be non-negative")
        if self.max_resources < 0:
            raise ValueError("max_resources must be non-negative")
        min_e, max_e = self.energy_range
        if min_e <= 0 or max_e <= 0:
            raise ValueError("energy_range must contain positive integers")
        if min_e > max_e:
            raise ValueError("energy_range min must be <= max")

    def spawn(self, world: WorldState, rng: RandomSource) -> list[Resource]:
        """Possibly spawn new resources into the world.

        Returns a list of newly created Resource objects that were added to the world.
        """

        if self.max_resources == 0 or self.spawn_rate <= 0.0:
            return []

        # Enforce cap based on current world contents.
        current = 0
        for e in world.iter_entities():
            if isinstance(e, Resource):
                current += 1
        if current >= self.max_resources:
            return []

        if rng.random() >= self.spawn_rate:
            return []

        x = rng.randint(0, world.grid.width - 1)
        y = rng.randint(0, world.grid.height - 1)
        pos = Position(x=x, y=y)

        min_e, max_e = self.energy_range
        energy = rng.randint(min_e, max_e)

        res = create_resource(position=pos, energy_value=energy)
        world.add_entity(res)
        return [res]
