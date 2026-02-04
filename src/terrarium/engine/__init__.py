"""Simulation execution engine.

This subpackage owns the simulation loop and coordination of world + entities.
"""

from __future__ import annotations

from .rng import DefaultRandom, SeededRNG
from .simulation import Simulation

# Backwards-compatibility alias expected by existing tests.
SimulationEngine = Simulation

__all__ = ["DefaultRandom", "SeededRNG", "Simulation", "SimulationEngine"]
