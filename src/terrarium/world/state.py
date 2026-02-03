"""World state container.

This module defines the central world state object that holds:
- The spatial grid
- The current simulation tick
- Entity collections with efficient lookup by ID and by position

Design constraints
------------------
- World state is the single source of truth for entity membership and location.
- No direct mutation of internal indices; use methods.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Protocol, Set

from terrarium.core.types import EntityId, Seed

from .grid import Grid, Position


class _WorldEntity(Protocol):
    """Minimum entity interface required by WorldState."""

    id: EntityId
    position: Position


@dataclass(slots=True)
class WorldState:
    """Central container for world state."""

    grid: Grid
    seed: Seed

    _tick: int = 0
    _entities_by_id: Dict[EntityId, _WorldEntity] = field(default_factory=dict)
    _entity_ids_by_pos: Dict[Position, Set[EntityId]] = field(default_factory=dict)

    @property
    def tick(self) -> int:
        """Current simulation timestep."""

        return self._tick

    def step_tick(self) -> int:
        """Increment tick counter by 1 and return the new tick."""

        self._tick += 1
        return self._tick

    def add_entity(self, entity: _WorldEntity) -> None:
        """Register an entity in the world.

        Notes
        -----
        - The entity's position is wrapped onto the grid.
        - Entity IDs must be unique.
        """

        if entity.id in self._entities_by_id:
            raise ValueError(f"Entity with id {entity.id!r} already exists")

        pos = self.grid.wrap(entity.position)
        # Ensure world is the source of truth for stored position.
        entity.position = pos

        self._entities_by_id[entity.id] = entity
        self._entity_ids_by_pos.setdefault(pos, set()).add(entity.id)

    def remove_entity(self, entity_id: EntityId) -> None:
        """Remove an entity by ID.

        Raises
        ------
        KeyError
            If the entity does not exist.
        """

        entity = self._entities_by_id.pop(entity_id)
        pos = entity.position

        ids = self._entity_ids_by_pos.get(pos)
        if ids is not None:
            ids.discard(entity_id)
            if not ids:
                self._entity_ids_by_pos.pop(pos, None)

    def get_entity(self, entity_id: EntityId) -> Optional[_WorldEntity]:
        """Retrieve an entity by ID."""

        return self._entities_by_id.get(entity_id)

    def get_entities_at(self, position: Position) -> List[_WorldEntity]:
        """Return entities at a given position (after wrapping)."""

        pos = self.grid.wrap(position)
        ids = self._entity_ids_by_pos.get(pos)
        if not ids:
            return []
        return [self._entities_by_id[eid] for eid in ids]

    def iter_entities(self) -> Iterable[_WorldEntity]:
        """Iterate over all entities (read-only view)."""

        return self._entities_by_id.values()
