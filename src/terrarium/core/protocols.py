"""Shared protocols.

Protocols in this module provide interfaces for core concepts without binding to
specific implementations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .types import EntityId


@runtime_checkable
class Entity(Protocol):
    """A simulation entity.

    Entities are objects that can exist in the world (e.g., organisms,
    resources). Implementations live in :mod:`terrarium.entities`.
    """

    @property
    def id(self) -> EntityId:
        """Stable identifier for the entity."""


@runtime_checkable
class RandomSource(Protocol):
    """RNG interface used by the engine.

    This protocol allows swapping deterministic RNGs for testing.
    """

    def randint(self, a: int, b: int) -> int:
        """Return random integer N such that a <= N <= b."""
