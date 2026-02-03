from __future__ import annotations

from typing import Dict, List, Optional, Protocol, Set

from terrarium.core.types import EntityId
from terrarium.engine.rng import SeededRNG
from terrarium.world.grid import Grid, Position


class _Entity(Protocol):
    @property
    def id(self) -> EntityId: ...

    @property
    def position(self) -> Position: ...


class WorldState:
    """Central container for world state.

    Holds:
    - the grid
    - a seeded RNG
    - current simulation tick
    - entities and a position->entity index

    Entities are treated as opaque objects that expose `id` and `position`.
    """

    def __init__(self, grid: Grid, *, seed: int) -> None:
        self.grid = grid
        self.rng = SeededRNG(seed)

        self._tick: int = 0
        self._entities: Dict[EntityId, _Entity] = {}
        self._pos_index: Dict[Position, Set[EntityId]] = {}

    @property
    def tick(self) -> int:
        return self._tick

    def step(self) -> int:
        """Advance the world's timestep and return the new tick value."""

        self._tick += 1
        return self._tick

    def add_entity(self, entity: _Entity) -> None:
        """Register an entity in the world."""

        eid = entity.id
        if eid in self._entities:
            # Minimal behavior: replace existing and keep indices consistent.
            self.remove_entity(eid)

        pos = self.grid.wrap(entity.position)
        self._entities[eid] = entity
        self._pos_index.setdefault(pos, set()).add(eid)

    def remove_entity(self, entity_id: EntityId) -> None:
        """Remove an entity by id. No-op if not present."""

        entity = self._entities.pop(entity_id, None)
        if entity is None:
            return

        pos = self.grid.wrap(entity.position)
        ids = self._pos_index.get(pos)
        if ids is None:
            return

        ids.discard(entity_id)
        if not ids:
            self._pos_index.pop(pos, None)

    def get_entity(self, entity_id: EntityId) -> Optional[_Entity]:
        return self._entities.get(entity_id)

    def get_entities_at(self, position: Position) -> List[_Entity]:
        pos = self.grid.wrap(position)
        ids = self._pos_index.get(pos)
        if not ids:
            return []
        # Preserve deterministic-ish order by insertion order of _entities.
        return [self._entities[eid] for eid in self._entities.keys() if eid in ids]
