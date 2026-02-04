from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Protocol, Set

from terrarium.core.types import EntityId
from terrarium.world.grid import Grid, Position


class _EntityLike(Protocol):
    """Minimal entity protocol for world state indexing."""

    id: EntityId
    position: Position


@dataclass(frozen=True, slots=True)
class _EntityRef:
    """Internal stable snapshot of an entity's indexed fields."""

    id: EntityId
    position: Position


class WorldState:
    """Central container for world state.

    Holds the grid, current simulation tick, and entity indexes.

    Notes:
    - Entities are indexed by ID for O(1) lookup.
    - Entities are also indexed by wrapped grid position for efficient spatial queries.
    - Internal indexes are only mutated via methods on this class.
    """

    def __init__(self, grid: Grid, seed: int) -> None:
        self.grid = grid
        self.seed = seed
        self._tick: int = 0

        self._entities: Dict[EntityId, object] = {}
        self._entity_refs: Dict[EntityId, _EntityRef] = {}
        self._pos_index: Dict[Position, Set[EntityId]] = {}

    @property
    def tick(self) -> int:
        return self._tick

    def step_tick(self) -> None:
        """Increment the simulation tick by 1."""

        self._tick += 1

    def add_entity(self, entity: _EntityLike) -> None:
        """Register an entity in the world."""

        entity_id = entity.id
        if entity_id in self._entities:
            raise ValueError(f"Entity with id {entity_id!r} already exists")

        pos = self.grid.wrap(entity.position)
        self._entities[entity_id] = entity
        self._entity_refs[entity_id] = _EntityRef(id=entity_id, position=pos)
        self._pos_index.setdefault(pos, set()).add(entity_id)

    def remove_entity(self, entity_id: EntityId) -> None:
        """Remove an entity by id.

        If the id is not present, this is a no-op.
        """

        ref = self._entity_refs.pop(entity_id, None)
        self._entities.pop(entity_id, None)
        if ref is None:
            return

        ids = self._pos_index.get(ref.position)
        if ids is None:
            return
        ids.discard(entity_id)
        if not ids:
            self._pos_index.pop(ref.position, None)

    def get_entity(self, entity_id: EntityId) -> Optional[object]:
        """Retrieve an entity by id."""

        return self._entities.get(entity_id)

    def get_entities_at(self, position: Position) -> List[object]:
        """Return entities at a given (wrapped) grid position."""

        pos = self.grid.wrap(position)
        ids = self._pos_index.get(pos)
        if not ids:
            return []
        # Keep deterministic order based on insertion order of dict by iterating over _entities
        return [self._entities[eid] for eid in ids if eid in self._entities]

    def iter_entities(self) -> Iterable[object]:
        """Iterate over all entities."""

        return self._entities.values()
