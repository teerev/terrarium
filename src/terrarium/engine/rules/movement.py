from __future__ import annotations

from dataclasses import dataclass

from terrarium.core.protocols import RandomSource
from terrarium.entities.organism import Organism
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(slots=True)
class MovementRule:
    """Rule for moving organisms one step per tick.

    Movement is random among wrapped adjacent neighbors plus the option to stay
    in place. Organisms are processed in a deterministic order (stable by UUID
    string form).
    """

    diagonals: bool = False
    allow_stay: bool = True

    def apply(self, organisms: list[Organism], world: WorldState, rng: RandomSource) -> None:
        # Deterministic processing order.
        organisms_sorted = sorted(organisms, key=lambda o: str(o.id))

        for org in organisms_sorted:
            current = world.grid.wrap(org.position)

            options = list(world.grid.neighbors(current, diagonals=self.diagonals))
            if self.allow_stay:
                options.append(current)

            if not options:
                continue

            idx = rng.randint(0, len(options) - 1)
            new_pos = world.grid.wrap(options[idx])

            if new_pos == current:
                # Ensure organism position is wrapped even if no movement.
                org.position = current
                continue

            # Update world's spatial index and organism position.
            world.remove_entity(org.id)
            org.position = new_pos
            world.add_entity(org)
