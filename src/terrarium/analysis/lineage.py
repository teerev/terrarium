from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Set

from terrarium.core.types import EntityId
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism


@dataclass(frozen=True, slots=True)
class OrganismRecord:
    """Immutable snapshot of organism lineage-relevant metadata at birth time."""

    id: EntityId
    parent_id: EntityId | None
    lineage_id: EntityId
    generation: int
    genome: Genome
    birth_tick: int
    death_tick: int | None = None


class LineageTree:
    """Track parent-child relationships and organism birth metadata.

    Design
    ------
    - Adjacency list for children: dict[parent_id, list[child_id]]
    - OrganismRecord stored per organism id
    - Deterministic updates: children appended in the order organisms are added
    """

    def __init__(self) -> None:
        self._children: Dict[EntityId, List[EntityId]] = {}
        self._records: Dict[EntityId, OrganismRecord] = {}

    def __len__(self) -> int:
        return len(self._records)

    def __iter__(self) -> Iterator[EntityId]:
        return iter(self._records.keys())

    def add_organism(self, organism: Organism) -> None:
        """Record an organism in the lineage tree.

        If the organism already exists, this is a no-op.
        """

        oid = organism.id
        if oid in self._records:
            return

        rec = OrganismRecord(
            id=oid,
            parent_id=organism.parent_id,
            lineage_id=organism.lineage_id,
            generation=int(organism.generation),
            genome=organism.genome,
            birth_tick=int(organism.birth_tick),
            death_tick=None,
        )
        self._records[oid] = rec

        if organism.parent_id is not None:
            self._children.setdefault(organism.parent_id, []).append(oid)

        # Ensure a key exists for the organism for fast get_children.
        self._children.setdefault(oid, [])

    def get_children(self, id: EntityId) -> List[EntityId]:
        """Return immediate children of *id* (deterministic order)."""

        return list(self._children.get(id, []))

    def get_ancestors(self, id: EntityId) -> List[EntityId]:
        """Return ancestor chain from parent up to the root.

        Order: [parent, grandparent, ...]
        """

        out: List[EntityId] = []
        cur = self._records.get(id)
        while cur is not None and cur.parent_id is not None:
            pid = cur.parent_id
            out.append(pid)
            cur = self._records.get(pid)
        return out

    def get_descendants(self, id: EntityId) -> List[EntityId]:
        """Return all descendants of *id* (depth-first, deterministic)."""

        result: List[EntityId] = []
        stack: List[EntityId] = list(reversed(self._children.get(id, [])))
        seen: Set[EntityId] = set()

        while stack:
            cid = stack.pop()
            if cid in seen:
                continue
            seen.add(cid)
            result.append(cid)

            kids = self._children.get(cid)
            if kids:
                # Reverse so left-to-right order remains stable with stack pop.
                stack.extend(reversed(kids))

        return result

    def get_organism_record(self, id: EntityId) -> OrganismRecord:
        rec = self._records.get(id)
        if rec is None:
            raise KeyError(id)
        return rec

    def mark_death(self, id: EntityId, tick: int) -> None:
        """Optionally record death tick for an organism already in the tree."""

        rec = self._records.get(id)
        if rec is None:
            return
        if rec.death_tick is not None:
            return
        self._records[id] = OrganismRecord(
            id=rec.id,
            parent_id=rec.parent_id,
            lineage_id=rec.lineage_id,
            generation=rec.generation,
            genome=rec.genome,
            birth_tick=rec.birth_tick,
            death_tick=int(tick),
        )

    def get_root(self, id: EntityId) -> Optional[EntityId]:
        """Return the top-most known ancestor for *id* (or None if unknown)."""

        if id not in self._records:
            return None
        cur_id = id
        while True:
            rec = self._records.get(cur_id)
            if rec is None or rec.parent_id is None:
                return cur_id
            if rec.parent_id not in self._records:
                return rec.parent_id
            cur_id = rec.parent_id
