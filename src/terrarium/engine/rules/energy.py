from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from terrarium.world.state import WorldState


class _HasEnergy(Protocol):
    @property
    def id(self): ...

    @property
    def energy(self) -> int: ...

    @energy.setter
    def energy(self, value: int) -> None: ...


@dataclass(frozen=True, slots=True)
class EnergyRule:
    """Apply baseline metabolism cost to organisms each tick.

    This rule is deterministic:
    - Uses a fixed per-tick cost (no randomness).
    - Applies in a stable order by organism id.

    Notes
    -----
    - Energy is floored at 0 and never becomes negative.
    - Death/removal at zero energy is handled elsewhere (future work orders).
    """

    metabolism_rate: int = 0

    def __post_init__(self) -> None:
        if int(self.metabolism_rate) < 0:
            raise ValueError("metabolism_rate must be non-negative")

    def apply(self, organisms: Iterable[_HasEnergy], world: WorldState) -> None:  # noqa: ARG002
        rate = int(self.metabolism_rate)
        if rate <= 0:
            return

        # Deterministic processing order: stable sort by id.
        ordered = sorted(list(organisms), key=lambda o: str(o.id))

        for org in ordered:
            current = int(org.energy)
            new_energy = current - rate
            if new_energy < 0:
                new_energy = 0
            org.energy = new_energy
