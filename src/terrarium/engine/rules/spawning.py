"""Resource spawning rules.

This module defines a deterministic resource spawner that can be integrated
into the simulation loop.

Design constraints
------------------
- Deterministic: all randomness comes from an injected RNG.
- Configurable: spawn rate, maximum resources, and energy range.
- Grid-bounded: positions are chosen within current world grid bounds.

Spawn model
-----------
Spawn rate is expressed as an expected spawns-per-tick value:
- The integer part spawns that many resources every tick.
- The fractional part spawns one additional resource with probability equal to
  the fractional part.

Examples:
- spawn_rate=0.25 => 25% chance of 1 spawn each tick.
- spawn_rate=1.0  => 1 spawn each tick.
- spawn_rate=2.5  => 2 spawns + 50% chance of a third each tick.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.entities.resource import Resource, create_resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class ResourceSpawner:
    """Spawn new resources into the world.

    Parameters
    ----------
    spawn_rate:
        Expected number of spawned resources per tick (must be >= 0).
    max_resources:
        Hard cap on number of resources allowed in the world (must be >= 0).
        If the current resource count is already at/above this cap, no spawning
        occurs.
    energy_range:
        Inclusive (min_energy, max_energy) for spawned resources.
    avoid_occupied:
        If True, attempt to avoid placing resources on already-occupied cells.
        If no free cell is found within a bounded number of attempts, spawning
        for that resource is skipped.
    """

    spawn_rate: float = 0.0
    max_resources: int = 0
    energy_range: tuple[int, int] = (1, 1)
    avoid_occupied: bool = True

    def __post_init__(self) -> None:
        if self.spawn_rate < 0:
            raise ValueError("spawn_rate must be >= 0")
        if self.max_resources < 0:
            raise ValueError("max_resources must be >= 0")
        lo, hi = self.energy_range
        if lo <= 0 or hi <= 0:
            raise ValueError("energy_range values must be positive")
        if lo > hi:
            raise ValueError("energy_range min must be <= max")

    def spawn(self, world: WorldState, rng: RandomSource) -> list[Resource]:
        """Spawn resources into *world* and return the created Resource objects."""

        cap_remaining = self.max_resources - self._count_resources(world)
        if cap_remaining <= 0:
            return []

        requested = self._draw_spawn_count(rng)
        to_spawn = min(requested, cap_remaining)
        if to_spawn <= 0:
            return []

        spawned: list[Resource] = []
        for _ in range(to_spawn):
            pos = self._draw_position(world, rng)
            if pos is None:
                continue
            energy = self._draw_energy(rng)
            # Ensure deterministic IDs by sourcing from the same seeded RNG.
            r = create_resource(pos, energy_value=energy, rng=rng)
            world.add_entity(r)
            spawned.append(r)
        return spawned

    def _draw_spawn_count(self, rng: RandomSource) -> int:
        base = int(self.spawn_rate)
        frac = float(self.spawn_rate - base)
        extra = 1 if (frac > 0 and rng.random() < frac) else 0
        return base + extra

    def _draw_energy(self, rng: RandomSource) -> int:
        lo, hi = self.energy_range
        # Use randint if available (SeededRNG provides it); otherwise fallback.
        randint = getattr(rng, "randint", None)
        if callable(randint):
            return int(randint(lo, hi))
        # Fallback deterministic mapping from random() into inclusive range.
        span = hi - lo + 1
        return int(lo + int(rng.random() * span))

    def _draw_position(self, world: WorldState, rng: RandomSource) -> Position | None:
        w, h = world.grid.width, world.grid.height
        randint = getattr(rng, "randint", None)

        def draw() -> Position:
            if callable(randint):
                return Position(int(randint(0, w - 1)), int(randint(0, h - 1)))
            return Position(int(rng.random() * w), int(rng.random() * h))

        if not self.avoid_occupied:
            return draw()

        # Try a bounded number of attempts to find an empty cell.
        max_attempts = max(1, w * h)
        for _ in range(max_attempts):
            pos = draw()
            if not world.get_entities_at(pos):
                return pos
        return None

    def _count_resources(self, world: WorldState) -> int:
        count = 0
        for e in world.iter_entities():
            # Avoid importing EntityType to keep this rule module lightweight.
            if getattr(e, "entity_type", None) == "resource":
                count += 1
            elif getattr(getattr(e, "entity_type", None), "value", None) == "resource":
                count += 1
        return count
