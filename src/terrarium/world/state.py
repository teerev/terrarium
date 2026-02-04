"""Central world state container.

The world state is the single source of truth for:
- The grid topology
- Entity storage and lookup (by id and by position)
- The current simulation tick

This module intentionally does not implement simulation logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Set

from terrarium.core.types import EntityId
from terrarium.world.grid import Grid, Position


class EntityLike(Protocol):
    """Minimal protocol for entities stored in the world."""

    @property
    def id(self) -> EntityId: ...

    @property
    def position(self) -> Position: ...


@dataclass(frozen=True)
class WorldState:
    """Central container for all world state.

    Args:
        grid: The grid used for wrapping and adjacency.
        seed: Seed value associated with this world's deterministic setup.
    """

    grid: Grid
    seed: int

    def __post_init__(self) -> None:
        # Internal mutable indexes. The dataclass is frozen, so we use
        # object.__setattr__ for initialization.
        object.__setattr__(self, "_tick", 0)
        object.__setattr__(self, "_entities", {})
        object.__setattr__(self, "_by_pos", {})
        object.__setattr__(self, "_lineage", None)

    @property
    def tick(self) -> int:
        """Current simulation timestep."""

        return self._tick

    def step(self) -> int:
        """Advance the simulation tick by one.

        Returns:
            The new tick value.
        """

        # WorldState is a frozen dataclass; mutate internal counter via object.__setattr__.
        new_tick = self._tick + 1
        object.__setattr__(self, "_tick", new_tick)
        return new_tick

    def set_lineage_tree(self, lineage_tree: object | None) -> None:
        """Attach a lineage tree to the world.

        The world will auto-record organism births when entities are added.

        This is intentionally typed as object to avoid importing the analysis
        subpackage from world state.
        """

        object.__setattr__(self, "_lineage", lineage_tree)

    def add_entity(self, entity: EntityLike) -> None:
        """Register an entity in the world."""

        entity_id = entity.id
        if entity_id in self._entities:
            raise ValueError(f"Entity id already exists: {entity_id}")

        pos = self.grid.wrap(entity.position)

        self._entities[entity_id] = entity
        self._by_pos.setdefault(pos, set()).add(entity_id)

        # Integrate with lineage tracking (auto-record births).
        # Avoid hard dependency on analysis module: use duck-typing.
        lt = getattr(self, "_lineage", None)
        if lt is not None and hasattr(lt, "add_organism"):
            try:
                lt.add_organism(entity)  # type: ignore[attr-defined]
            except Exception:
                # World state must not fail to add entities due to optional analytics.
                pass

    def remove_entity(self, entity_id: EntityId) -> None:
        """Remove an entity from the world by id."""

        entity = self._entities.pop(entity_id, None)
        if entity is None:
            return

        pos = self.grid.wrap(entity.position)
        ids = self._by_pos.get(pos)
        if ids is not None:
            ids.discard(entity_id)
            if not ids:
                self._by_pos.pop(pos, None)

    def move_entity(self, entity_id: EntityId, new_position: Position) -> None:
        """Move an entity to a new position and update spatial index."""

        entity = self._entities.get(entity_id)
        if entity is None:
            return

        old_pos = self.grid.wrap(entity.position)
        new_pos = self.grid.wrap(new_position)

        if old_pos == new_pos:
            return

        # Update index: remove from old position
        old_ids = self._by_pos.get(old_pos)
        if old_ids is not None:
            old_ids.discard(entity_id)
            if not old_ids:
                self._by_pos.pop(old_pos, None)

        # Update entity position (entities are expected to have a setter)
        setattr(entity, "position", new_pos)

        # Update index: add to new position
        self._by_pos.setdefault(new_pos, set()).add(entity_id)

    def get_entity(self, entity_id: EntityId) -> Optional[EntityLike]:
        """Retrieve an entity by id."""

        return self._entities.get(entity_id)

    def get_entities_at(self, position: Position) -> List[EntityLike]:
        """Return a list of entities currently indexed at a position."""

        pos = self.grid.wrap(position)
        ids = self._by_pos.get(pos, set())
        return [self._entities[eid] for eid in ids if eid in self._entities]


# Internal attribute type hints (for static checkers)
WorldState._tick: int
WorldState._entities: Dict[EntityId, EntityLike]
WorldState._by_pos: Dict[Position, Set[EntityId]]
WorldState._lineage: object | None
