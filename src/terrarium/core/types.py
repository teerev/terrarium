from __future__ import annotations

"""Shared type aliases for the terrarium simulation.

These aliases are used across subpackages to keep interfaces stable while the
implementation evolves.
"""

from typing import NewType, Tuple

EntityId = NewType("EntityId", str)
"""Stable identifier for an entity within a simulation."""

Position = Tuple[int, int]
"""Grid position in (x, y) coordinates."""
