from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set

from terrarium.entities.base import EntityId
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism


@dataclass(frozen=True, slots=True)
class OrganismRecord:
    """Snapshot of an organism at birth time.

    Notes:
        - genome is stored as a value (Genome is immutable) to preserve birth snapshot.
        - death_tick is optional and can be set later.
    """

    id: EntityId
    parent_id: EntityId | None
    genome: Genome
    birth_tick: int
    death_tick: int | None = None


class LineageTree:
    """Track parent-child relationships and organism birth metadata."""

    def __init__(self) -> None:
        self._children: Dict[EntityId, List[EntityId]] = {}
        self._parent: Dict[EntityId, EntityId | None] = {}
        self._records: Dict[EntityId, OrganismRecord] = {}
        self._seen: Set[EntityId] = set()

    def __iter__(self) -> Iterable[EntityId]:
        return iter(self._records.keys())

    def add_organism(self, organism: Organism) -> None:
        """Record an organism in the tree.

        This method is idempotent for a given organism id.
        """

        oid = organism.id
        # Organism.id is declared as EntityId | None, but should always be set.
        if oid is None:  # pragma: no cover
            raise ValueError("Organism id must not be None")

        if oid in self._seen:
            return
        self._seen.add(oid)

        parent_id = organism.parent_id
        self._parent[oid] = parent_id

        if parent_id is not None:
            self._children.setdefault(parent_id, []).append(oid)
        self._children.setdefault(oid, [])

        # Snapshot at birth time.
        self._records[oid] = OrganismRecord(
            id=oid,
            parent_id=parent_id,
            genome=organism.genome,
            birth_tick=int(organism.birth_tick),
            death_tick=None,
        )

    def mark_dead(self, organism_id: EntityId, death_tick: int) -> None:
        """Optional: mark an organism as dead while keeping it in the tree."""

        rec = self._records.get(organism_id)
        if rec is None:
            return
        if rec.death_tick is not None:
            return
        self._records[organism_id] = OrganismRecord(
            id=rec.id,
            parent_id=rec.parent_id,
            genome=rec.genome,
            birth_tick=rec.birth_tick,
            death_tick=int(death_tick),
        )

    def get_children(self, organism_id: EntityId) -> List[EntityId]:
        """Return the immediate children of an organism."""

        return list(self._children.get(organism_id, []))

    def get_ancestors(self, organism_id: EntityId) -> List[EntityId]:
        """Return the ancestor chain, ordered from parent -> ... -> root."""

        ancestors: List[EntityId] = []
        cur: Optional[EntityId] = organism_id
        while True:
            p = self._parent.get(cur)
            if p is None:
                break
            ancestors.append(p)
            cur = p
        return ancestors

    def get_descendants(self, organism_id: EntityId) -> List[EntityId]:
        """Return all descendants (depth-first), excluding the provided id."""

        out: List[EntityId] = []
        stack: List[EntityId] = list(self._children.get(organism_id, []))
        while stack:
            nid = stack.pop()
            out.append(nid)
            kids = self._children.get(nid)
            if kids:
                stack.extend(kids)
        return out

    def get_organism_record(self, organism_id: EntityId) -> OrganismRecord:
        rec = self._records.get(organism_id)
        if rec is None:
            raise KeyError(organism_id)
        return rec
