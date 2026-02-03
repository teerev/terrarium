from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Protocol, Set, TypeVar, Union, runtime_checkable

from .grid import Grid, Position


EntityId = Union[int, str]


@runtime_checkable
class Entity(Protocol):
    """Minimal entity protocol for WorldState.

    Entities must have an immutable/stable 'id' and a current 'position'.
    """

    id: EntityId
    position: Position


TEntity = TypeVar("TEntity", bound=Entity)


class WorldState:
    """Central container for world state.

    Holds:
    - the grid
    - current simulation tick
    - entity registry and a position index

    Mutation of state should happen only through methods on this class.
    """

    def __init__(self, grid: Grid, seed: int | None = None) -> None:
        self.grid = grid
        self.seed = seed
        self._tick: int = 0

        self._entities: Dict[EntityId, Entity] = {}
        self._pos_index: Dict[Position, Set[EntityId]] = {}

    @property
    def tick(self) -> int:
        return self._tick

    def step(self) -> int:
        """Advance the world's timestep by 1 and return the new tick."""

        self._tick += 1
        return self._tick

    def add_entity(self, entity: Entity) -> None:
        """Register an entity in the world.

        If an entity with the same id already exists, it is replaced.
        """

        pos = self.grid.wrap(entity.position)

        # If replacing, remove old index entry first.
        existing = self._entities.get(entity.id)
        if existing is not None:
            self._discard_from_index(entity.id, self.grid.wrap(existing.position))

        # Store entity and index under wrapped position.
        # Note: We do not mutate the entity; index uses wrapped position for queries.
        self._entities[entity.id] = entity
        self._pos_index.setdefault(pos, set()).add(entity.id)

    def remove_entity(self, entity_id: EntityId) -> None:
        """Remove an entity by id. No-op if the id is not present."""

        ent = self._entities.pop(entity_id, None)
        if ent is None:
            return
        self._discard_from_index(entity_id, self.grid.wrap(ent.position))

    def get_entity(self, entity_id: EntityId) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def get_entities_at(self, position: Position) -> List[Entity]:
        """Return entities at the given position.

        Position is wrapped to the grid.
        """

        pos = self.grid.wrap(position)
        ids = self._pos_index.get(pos)
        if not ids:
            return []
        # Deterministic order for tests/callers.
        return [self._entities[eid] for eid in sorted(ids, key=lambda x: str(x)) if eid in self._entities]

    def all_entities(self) -> List[Entity]:
        """Return all entities currently registered (deterministic order)."""

        return [self._entities[eid] for eid in sorted(self._entities.keys(), key=lambda x: str(x))]

    def _discard_from_index(self, entity_id: EntityId, pos: Position) -> None:
        bucket = self._pos_index.get(pos)
        if not bucket:
            return
        bucket.discard(entity_id)
        if not bucket:
            self._pos_index.pop(pos, None)
