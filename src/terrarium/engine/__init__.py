"""Simulation engine for terrarium.

The engine subpackage owns the simulation loop and coordinates updates across
world and entities. Implementations are intentionally placeholders for now.
"""

from __future__ import annotations

from .rng import DefaultRandom, SeededRNG
from .simulation import Simulation

__all__ = ["DefaultRandom", "SeededRNG", "Simulation"]
