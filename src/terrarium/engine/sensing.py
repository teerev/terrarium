from __future__ import annotations

from typing import Iterable, Protocol

from terrarium.entities.resource import Resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


class _HasPosition(Protocol):
    @property
    def position(self) -> Position: ...


class _HasPhenotypeSense(Protocol):
    @property
    def phenotype(self): ...


def sense_nearby_resources(organism: _HasPosition | _HasPhenotypeSense, world: WorldState) -> list[Resource]:
    """Return resources within the organism's sensing range.

    - Range is determined by organism.phenotype.sense_range.
    - Uses world.grid.distance(), which is toroidal Manhattan distance.
    - Deterministic given world state.
    - Returns resources sorted by distance (nearest first), stable for ties.

    If sense_range <= 0 or missing, returns [].
    """

    phenotype = getattr(organism, "phenotype", None)
    sense_range = int(getattr(phenotype, "sense_range", 0) or 0)
    if sense_range <= 0:
        return []

    origin = world.grid.wrap(getattr(organism, "position"))

    # Iterate deterministically by stable entity id ordering.
    entities: Iterable[object] = list(world._entities.values())  # type: ignore[attr-defined]
    resources: list[Resource] = []
    for ent in sorted(entities, key=lambda e: str(getattr(e, "id", ""))):
        if not isinstance(ent, Resource):
            continue
        if bool(getattr(ent, "consumed", False)):
            continue

        d = int(world.grid.distance(origin, world.grid.wrap(ent.position)))
        if d <= sense_range:
            resources.append(ent)

    # Sort by distance (then stable by id).
    resources.sort(key=lambda r: (int(world.grid.distance(origin, world.grid.wrap(r.position))), str(r.id)))
    return resources


def sense_nearby(organism: _HasPosition | _HasPhenotypeSense, world: WorldState) -> list[Resource]:
    """Backward-compatible alias for sense_nearby_resources."""

    return sense_nearby_resources(organism, world)
