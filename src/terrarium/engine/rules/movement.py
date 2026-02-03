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


class _HasPhenotypeSpeed(Protocol):
    @property
    def phenotype(self): ...


class _HasEnergy(Protocol):
    @property
    def energy(self) -> int: ...

    @energy.setter
    def energy(self, value: int) -> None: ...


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

    # Public API: base movement cost (energy units). Actual cost scales by speed.
    base_movement_cost: int = 1

    def apply(self, organisms: Iterable[_Movable], world: WorldState, rng: SeededRNG) -> None:
        # Deterministic processing order: stable sort by id.
        ordered = sorted(list(organisms), key=lambda o: str(o.id))

        for org in ordered:
            # Speed controls probability of attempting movement each tick.
            # Design constraint: speed=0 => never moves, speed=1 => always moves.
            speed = float(getattr(getattr(org, "phenotype", None), "speed", 1.0))
            if speed < 0.0:
                speed = 0.0
            if speed > 1.0:
                speed = 1.0

            # Speed=0 -> never move. Speed=1 -> always move.
            if rng.random() >= speed:
                continue

            current = world.grid.wrap(org.position)
            candidates = world.grid.neighbors(current, diagonal=self.diagonal)
            if self.allow_stay:
                candidates = [current, *candidates]

            # choice() is deterministic given RNG state and candidate list order.
            new_pos = rng.choice(candidates)
            world.move_entity(org.id, new_pos)

            # Energy cost scales with speed; apply only when a move was attempted.
            cost = int(round(int(self.base_movement_cost) * speed))
            if cost <= 0:
                continue

            if hasattr(org, "energy"):
                try:
                    org.energy = int(getattr(org, "energy")) - cost  # type: ignore[attr-defined]
                except Exception:
                    pass
