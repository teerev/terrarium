"""Entity definitions.

The entities subpackage defines the objects that exist within the world such as
organisms and resources.
"""

from __future__ import annotations

from .base import Entity
from .organism import Organism
from .resource import Resource

__all__ = [
    "Entity",
    "Organism",
    "Resource",
]
