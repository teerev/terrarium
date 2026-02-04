from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.organism import Organism
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class EnergyRule:
    """Rule for applying baseline metabolism energy drain.

    Design constraints:
    - Deterministic (fixed cost per tick, no randomness)
    - All organisms pay the same metabolism cost
    - Energy cannot go below 0

    Public API:
    - EnergyRule.metabolism_rate -> int
    - EnergyRule.apply(organisms, world) -> None
    """

    metabolism_rate: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.metabolism_rate, int) or self.metabolism_rate < 0:
            raise ValueError("metabolism_rate must be a non-negative integer")

    def apply(self, organisms: list[Organism], world: WorldState) -> None:
        """Drain energy from each organism once, in the given order."""

        if self.metabolism_rate == 0:
            return

        for org in organisms:
            # Floor at 0 (no negative energy).
            new_energy = org.energy - self.metabolism_rate
            org.energy = 0 if new_energy < 0 else new_energy
