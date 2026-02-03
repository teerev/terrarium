from __future__ import annotations

from .consumption import ConsumptionRule
from .death import DeathRule
from .energy import EnergyRule
from .movement import MovementRule
from .reproduction import ReproductionRule
from .spawning import ResourceSpawner

__all__ = [
    "ConsumptionRule",
    "DeathRule",
    "EnergyRule",
    "MovementRule",
    "ReproductionRule",
    "ResourceSpawner",
]
