"""Organism movement rules.

Scope (P1.09)
------------
- Basic random movement: choose a random adjacent cell (4-neighborhood)
- Optionally allow staying in place
- Deterministic: all randomness comes from injected RNG
- Grid wrapping handled by Grid.neighbors()/Grid.wrap
- Updates WorldState spatial index when entities move

Out of scope
------------
- Collision detection
- Movement costs / speed
- Directed movement
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from terrarium.core.protocols import RandomSource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


class _Movable(Protocol):
    """Minimum interface for something that can be moved by this rule."""

    id: object
    position: Position


@dataclass(frozen=True, slots=True)
class MovementRule:
    """Move organisms randomly to a neighboring cell.

    Parameters
    ----------
    include_stay:
        If True, staying in place is included as a movement option.
    adjacency:
        Neighborhood to use (4 or 8). Default is 4 per work order.
    """

    include_stay: bool = True
    adjacency: int = 4

    def apply(self, organisms: Sequence[_Movable], world: WorldState, rng: RandomSource) -> None:
        """Apply movement to all organisms exactly once, in the given order."""

        for o in organisms:
            current = world.grid.wrap(o.position)
            options = list(world.grid.neighbors(current, adjacency=self.adjacency))
            if self.include_stay:
                options.append(current)

            # Use choice if available; otherwise map random() to an index.
            choice = getattr(rng, "choice", None)
            if callable(choice):
                target = choice(options)
            else:
                idx = int(rng.random() * len(options))
                if idx >= len(options):
                    idx = len(options) - 1
                target = options[idx]

            # Ensure wrapping (neighbors already wrapped, but keep invariant explicit).
            target = world.grid.wrap(target)
            if target != current:
                world.move_entity(o.id, target)
