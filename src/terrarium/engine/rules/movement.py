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

    Public API:
    - MovementRule.apply(organisms, world, rng) -> None
    """

    allow_stay: bool = True
    diagonals: bool = True

    def apply(self, organisms: list[Organism], world: WorldState, rng: SeededRNG) -> None:
        """Move each organism once, in the given order."""

        for org in organisms:
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
