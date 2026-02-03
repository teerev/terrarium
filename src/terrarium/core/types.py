"""Shared type aliases.

These types are intentionally lightweight and stable to avoid circular imports.
"""

from __future__ import annotations

from typing import NewType

Coord = tuple[int, int]

EntityId = NewType("EntityId", int)
