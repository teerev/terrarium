"""Simulation execution engine.

This subpackage owns the simulation loop and coordination of world + entities.
"""

from __future__ import annotations

from .rng import DefaultRandom
from .simulation import SimulationEngine

__all__ = ["DefaultRandom", "SimulationEngine"]
