"""Resource entity placeholder.

Resources represent non-living consumables or environmental features.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import Entity


@dataclass(slots=True)
class Resource(Entity):
    """A non-living entity.

    Placeholder: will later include quantity, regeneration, and interaction rules.
    """

    quantity: float = 0.0
