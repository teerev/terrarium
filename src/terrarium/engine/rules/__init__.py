"""Engine rules.

Rules are optional components that mutate world state as part of the simulation
loop (e.g., spawning resources).
"""

from __future__ import annotations

from .energy import EnergyRule
from .movement import MovementRule
from .spawning import ResourceSpawner

__all__ = [
    "ResourceSpawner",
    "MovementRule",
    "EnergyRule",
]
