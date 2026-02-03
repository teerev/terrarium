"""Resource entity placeholder.

Resources are passive entities or quantities that organisms may consume.
"""

from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.base import Entity


@dataclass(slots=True)
class Resource(Entity):
    """A placeholder resource type."""
