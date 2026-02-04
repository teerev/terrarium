"""Simulation execution engine.

This subpackage hosts the simulation loop, scheduling, and randomness plumbing.
Implementations are placeholders only.
"""

from __future__ import annotations

from .rng import DefaultRNG, SeededRNG
from .simulation import Simulation
from . import rules

__all__ = [
    "DefaultRNG",
    "SeededRNG",
    "Simulation",
    "rules",
]
