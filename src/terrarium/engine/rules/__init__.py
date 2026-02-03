"""Engine rules.

Rules are optional, composable components that apply deterministic logic during
simulation steps.
"""

from __future__ import annotations

from .consumption import ConsumptionRule
from .energy import EnergyRule
from .movement import MovementRule
from .spawning import ResourceSpawner

__all__ = ["ConsumptionRule", "EnergyRule", "MovementRule", "ResourceSpawner"]
