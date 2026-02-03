"""Organism entity placeholder.

Organisms are active entities that may act each simulation step.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.base import Entity


@dataclass(slots=True)
class Organism(Entity):
    """A placeholder organism type."""
