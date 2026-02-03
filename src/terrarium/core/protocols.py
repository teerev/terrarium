"""Core protocols.

Protocols define small interfaces that multiple concrete implementations can
conform to without introducing hard dependencies.
"""

from __future__ import annotations

from typing import Protocol

from .types import EntityId


class HasId(Protocol):
    """An object that exposes a stable entity identifier."""

    @property
    def id(self) -> EntityId:
        """Return the stable identifier."""


class SupportsRng(Protocol):
    """An object that provides access to a random number generator."""

    def random(self) -> float:
        """Return the next random float in the range [0.0, 1.0)."""
