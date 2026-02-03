"""Organism entity placeholder.

Organisms represent living agents in the simulation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Entity


@dataclass(slots=True)
class Organism(Entity):
    """A living entity.

    Placeholder: will later include traits, energy, and decision-making state.
    """

    energy: float = 0.0
