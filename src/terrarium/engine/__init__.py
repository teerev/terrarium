"""Simulation execution engine.

This subpackage hosts the simulation loop, scheduling, and randomness plumbing.
Implementations are placeholders only.
"""

from __future__ import annotations

from .rng import DefaultRNG
from .simulation import Simulation

__all__ = [
    "DefaultRNG",
    "Simulation",
]
