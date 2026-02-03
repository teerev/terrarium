"""Base entity definitions.

Concrete entities (organisms, resources, etc.) can share common functionality by
subclassing :class:`~terrarium.entities.base.BaseEntity`.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.core import EntityId


@dataclass(frozen=True, slots=True)
class BaseEntity:
    """Minimal concrete entity.

    Serves as a simple implementation of the core :class:`terrarium.core.Entity`
    protocol.
    """

    id: EntityId
