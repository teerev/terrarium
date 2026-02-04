from __future__ import annotations

"""Organism entity.

A minimal placeholder for a living entity in the simulation.
"""

from dataclasses import dataclass

from terrarium.entities.base import Entity


@dataclass(slots=True)
class Organism(Entity):
    """A living entity.

    Future implementations may include metabolism, reproduction, and behavior.
    """
