"""Energy (metabolism) rule.

Scope (P1.10)
------------
- Deterministic baseline metabolism cost per tick that drains energy.
- All organisms pay the same fixed cost.
- Cost is configurable at construction time.
- Energy floors at 0 (never negative).

Out of scope
------------
- Energy gain from consumption
- Movement/reproduction costs
- Death handling when energy reaches 0

Tick order
----------
This rule is intended to run at a defined point during Simulation.step().
Current integration runs metabolism after movement and before other (future)
interaction phases.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from terrarium.world.state import WorldState


class _HasEnergy(Protocol):
    """Minimum interface required for metabolism energy drain."""

    energy: int


@dataclass(frozen=True, slots=True)
class EnergyRule:
    """Apply baseline metabolism cost to all organisms.

    Parameters
    ----------
    metabolism_rate:
        Fixed energy cost per tick applied to every organism. Must be >= 0.
    """

    metabolism_rate: int = 0

    def __post_init__(self) -> None:
        if self.metabolism_rate < 0:
            raise ValueError("metabolism_rate must be >= 0")

    def apply(self, organisms: Sequence[_HasEnergy], world: WorldState) -> None:
        """Drain energy from each organism in the given deterministic order.

        Energy is floored at 0.

        Parameters
        ----------
        organisms:
            Organisms to apply metabolism to.
        world:
            WorldState is accepted for future extensibility/observability.
            It is not mutated by this rule.
        """

        rate = int(self.metabolism_rate)
        if rate <= 0:
            return

        for o in organisms:
            # Floor at 0; never negative.
            new_energy = int(getattr(o, "energy")) - rate
            o.energy = 0 if new_energy < 0 else new_energy
