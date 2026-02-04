from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(slots=True)
class EnergyRule:
    """Rule applying baseline metabolism energy drain each tick.

    Notes
    -----
    - Deterministic: fixed energy cost per tick.
    - Applied to all organisms in a deterministic order (stable by UUID string).
    - Energy is floored at 0 (never negative).
    """

    metabolism_rate: int = 1

    def __post_init__(self) -> None:
        if self.metabolism_rate < 0:
            raise ValueError("metabolism_rate must be non-negative")

    def apply(self, organisms: list[Organism], world: WorldState) -> None:
        # `world` is currently unused but kept for the public API and future needs.
        _ = world

        if self.metabolism_rate == 0:
            return

        organisms_sorted = sorted(organisms, key=lambda o: str(o.id))
        for org in organisms_sorted:
            org.energy = max(0, org.energy - self.metabolism_rate)
