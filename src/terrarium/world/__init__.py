"""World state management.

The world subpackage is responsible for representing the simulation space
(e.g., a grid) and the state that evolves over time.
"""

from __future__ import annotations

from .grid import Grid
from .state import WorldState

__all__ = [
    "Grid",
    "WorldState",
]
