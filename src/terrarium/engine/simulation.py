"""Simulation loop placeholders.

The engine orchestrates stepping the world forward in time. This file only
defines a placeholder class with a minimal API.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.world import WorldState


@dataclass(slots=True)
class Simulation:
    """A minimal simulation wrapper.

    Later milestones will add stepping, scheduling, and event handling.
    """

    state: WorldState
