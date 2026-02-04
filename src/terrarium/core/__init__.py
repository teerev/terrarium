"""Core shared types and protocols.

This subpackage defines type aliases and Protocol-based interfaces used across the
simulation. It should not depend on higher-level modules such as engine/world.
"""

from __future__ import annotations

from .protocols import RandomSource
from .types import EntityId, Position

__all__ = ["EntityId", "Position", "RandomSource"]
