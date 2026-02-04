from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.entities.organism import Organism
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class MovementRule:
    """Rule for moving organisms randomly to adjacent cells.

    Design:
    - Deterministic via provided RNG
    - Adjacent movement only (uses Grid.neighbors)
    - Wrapping handled by Grid
    - Optionally allows staying in place

    Genome-driven movement (P2.07):
    - Per-tick probability of attempting movement is organism.phenotype.speed
    - speed=0 -> never moves; speed=1 -> always attempts to move
    - If speed > 1.0 (possible due to phenotype scaling), it is treated as 1.0
    - Energy cost is proportional to speed when movement occurs

    Public API:
    - MovementRule.apply(organisms, world, rng) -> None
    - MovementRule.base_movement_cost -> int
    """

    allow_stay: bool = True
    diagonals: bool = True
    base_movement_cost: int = 1

    def _bernoulli(self, rng: SeededRNG, p: float) -> bool:
        """Deterministic Bernoulli(p) using whichever RNG API is available.

        Some unit tests provide minimal RNG stubs that only implement `choice`.
        Prefer `rng.random()` when present; otherwise fall back to `choice`.
        """

        if p <= 0.0:
            return False
        if p >= 1.0:
            return True

        rnd = getattr(rng, "random", None)
        if callable(rnd):
            return float(rnd()) < p

        # Fallback: approximate probability using a discrete draw.
        # Using choice avoids requiring randint.
        n = 100
        k = int(p * n)
        if k <= 0:
            return False
        if k >= n:
            return True
        return bool(rng.choice([True] * k + [False] * (n - k)))

    def apply(self, organisms: list[Organism], world: WorldState, rng: SeededRNG) -> None:
        """Move each organism at most once, in the given order."""

        for org in organisms:
            speed = float(getattr(org.phenotype, "speed", 0.0))
            if speed <= 0.0:
                continue

            # Speed 1 = always moves; clamp to [0, 1] for probability.
            p_move = min(1.0, speed)

            if not self._bernoulli(rng, p_move):
                continue

            current = world.grid.wrap(org.position)

            # Neighbor ordering matters for determinism and for tests that use a
            # fixed RNG selecting seq[0]. For 4-way movement, the expected order
            # is (-1,0), (1,0), (0,-1), (0,1).
            if self.diagonals:
                options = world.grid.neighbors8(current)
            else:
                x0, y0 = current.x, current.y
                options = [
                    world.grid.wrap(Position(x0 - 1, y0)),
                    world.grid.wrap(Position(x0 + 1, y0)),
                    world.grid.wrap(Position(x0, y0 - 1)),
                    world.grid.wrap(Position(x0, y0 + 1)),
                ]

            if self.allow_stay:
                options = [current] + options

            target: Position = rng.choice(options)
            if target == current:
                continue

            world.move_entity(org.id, target)

            # Movement costs energy proportional to speed.
            # Keep as an integer decrement for consistency with other rules.
            cost = int(round(float(self.base_movement_cost) * float(speed)))
            if cost > 0:
                org.energy = max(0, int(org.energy) - cost)
