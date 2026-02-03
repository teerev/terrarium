from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.resource import Resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ResourceSpawner:
    """Spawn rule for Resource entities.

    Parameters
    ----------
    spawn_rate:
        Probability per tick to attempt a single spawn.
    max_resources:
        Hard cap on the number of Resource entities allowed in the world.
    energy_range:
        Inclusive (min, max) energy value range for spawned resources.

    Notes
    -----
    - Deterministic given the same RNG state.
    - Spawns at a uniformly random grid position.
    - Avoids spawning on positions already occupied by any entity.
    """

    spawn_rate: float = 0.0
    max_resources: int = 0
    energy_range: tuple[int, int] = (1, 1)

    def __post_init__(self) -> None:
        if float(self.spawn_rate) < 0.0:
            raise ValueError("spawn_rate must be non-negative")
        if int(self.max_resources) < 0:
            raise ValueError("max_resources must be non-negative")

        lo, hi = self.energy_range
        lo_i = int(lo)
        hi_i = int(hi)
        if lo_i <= 0 or hi_i <= 0:
            raise ValueError("energy_range values must be positive")
        if lo_i > hi_i:
            raise ValueError("energy_range min must be <= max")

    def spawn(self, world: WorldState, rng: SeededRNG) -> list[Resource]:
        """Possibly spawn new resources into the world.

        Returns a list of created resources (also added to world).
        """

        if self.max_resources == 0:
            return []

        # Respect cap based on current Resource count.
        existing_resources = 0
        for ent in world._entities.values():  # type: ignore[attr-defined]
            if getattr(ent, "entity_type", None) is not None and str(getattr(ent, "entity_type")) == "EntityType.RESOURCE":
                existing_resources += 1
            elif getattr(ent, "entity_type", None) == "resource":
                existing_resources += 1
            else:
                # Fallback for current codebase: Resource instances.
                if isinstance(ent, Resource):
                    existing_resources += 1

        if existing_resources >= self.max_resources:
            return []

        rate = float(self.spawn_rate)
        if rate <= 0.0:
            return []

        if rng.random() >= rate:
            return []

        # Find an unoccupied random position (bounded attempts).
        width = world.grid.width
        height = world.grid.height
        max_attempts = max(1, min(32, width * height))

        pos: Position | None = None
        for _ in range(max_attempts):
            x = rng.randint(0, width - 1)
            y = rng.randint(0, height - 1)
            candidate = Position(x, y)
            if not world.get_entities_at(candidate):
                pos = candidate
                break

        if pos is None:
            return []

        lo, hi = self.energy_range
        energy = rng.randint(int(lo), int(hi))
        res = Resource(position=pos, energy_value=energy)
        world.add_entity(res)
        return [res]
