from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from terrarium.engine.rng import SeededRNG
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


class _Movable(Protocol):
    @property
    def id(self): ...

    @property
    def position(self) -> Position: ...

    @position.setter
    def position(self, value: Position) -> None: ...


@dataclass(frozen=True, slots=True)
class MovementRule:
    """Basic random movement rule.

    - Each organism chooses uniformly from neighboring cells plus "stay".
    - Neighbor computation uses Grid.neighbors(), which wraps at boundaries.
    - Deterministic given the same organism order and RNG state.

    Notes
    -----
    - Collision handling is intentionally out of scope.
    """

    diagonal: bool = False
    allow_stay: bool = True

    def apply(self, organisms: Iterable[_Movable], world: WorldState, rng: SeededRNG) -> None:
        # Deterministic processing order: stable sort by id.
        ordered = sorted(list(organisms), key=lambda o: str(o.id))

        for org in ordered:
            current = world.grid.wrap(org.position)
            candidates = world.grid.neighbors(current, diagonal=self.diagonal)
            if self.allow_stay:
                candidates = [current, *candidates]

            # choice() is deterministic given RNG state and candidate list order.
            new_pos = rng.choice(candidates)
            world.move_entity(org.id, new_pos)
