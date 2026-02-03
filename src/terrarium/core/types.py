"""Shared type aliases.

Only lightweight, broadly reusable types should live here to avoid circular
imports between major subpackages.
"""

from __future__ import annotations

from typing import NewType, Tuple

EntityId = NewType("EntityId", str)
"""A stable identifier for an entity within a simulation."""

Position = Tuple[int, int]
"""A 2D grid position expressed as (x, y)."""
