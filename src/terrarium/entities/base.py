"""Base entity protocol and identifiers.

This module defines the minimal interface (contract) that all simulation entities
must satisfy. Entities are intentionally modeled via ``typing.Protocol`` for
structural subtyping to avoid inheritance-heavy designs.

Contract
--------
An entity must provide:
- ``id``: an immutable unique identifier (EntityId)
- ``position``: gettable and settable spatial position
- ``entity_type``: a coarse category for filtering/grouping

The protocol is designed to be compatible with mypy structural typing.
"""

from __future__ import annotations

from enum import Enum
from typing import Protocol, runtime_checkable
from uuid import UUID

from terrarium.core.protocols import RandomSource
from terrarium.world.grid import Position

EntityId = UUID
"""Immutable unique identifier for an entity.

Entity IDs must be deterministic when simulation determinism is required.
"""


class EntityType(str, Enum):
    """Coarse entity categories.

    This enables filtering/grouping without relying on concrete classes.
    """

    ORGANISM = "organism"
    RESOURCE = "resource"


def generate_id(rng: RandomSource | None = None) -> EntityId:
    """Generate a new unique entity id.

    Determinism requirement
    -----------------------
    If *rng* is provided, IDs are generated deterministically from that RNG.
    If *rng* is not provided, a deterministic simulation is not guaranteed.

    Notes
    -----
    We avoid uuid.uuid4() here because it sources OS randomness.
    """

    if rng is None:
        # Preserve historical behavior for ad-hoc usage, but this is not
        # deterministic across process restarts.
        from uuid import uuid4

        return uuid4()

    randint = getattr(rng, "randint", None)
    if not callable(randint):
        raise TypeError("rng must provide randint(a, b) to generate deterministic entity ids")

    return UUID(int=int(randint(0, (1 << 128) - 1)))


@runtime_checkable
class Entity(Protocol):
    """Base protocol that all simulation entities must implement."""

    @property
    def id(self) -> EntityId:
        """Immutable unique entity identifier."""

    @property
    def position(self) -> Position:
        """Current entity position."""

    @position.setter
    def position(self, value: Position) -> None:
        """Update entity position."""

    @property
    def entity_type(self) -> EntityType:
        """Entity category."""
