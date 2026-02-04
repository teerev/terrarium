from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.grid import Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class SensedResource:
    """A resource along with its (toroidal) Manhattan distance from an organism."""

    resource: Resource
    distance: int


def sense_nearby_resources(organism: Organism, world: WorldState) -> list[Resource]:
    """Return unconsumed resources within the organism's sensing range.

    - Range is determined by organism.phenotype.sense_range
    - Uses the world's toroidal Manhattan distance (Grid.distance)
    - Deterministic given world state
    - Returned list is sorted by (distance, resource_id) for stable ordering

    If sense_range <= 0, returns [].
    """

    sense_range = int(getattr(organism.phenotype, "sense_range", 0))
    if sense_range <= 0:
        return []

    origin: Position = world.grid.wrap(organism.position)

    sensed: list[tuple[int, str, Resource]] = []
    for e in getattr(world, "_entities", {}).values():
        if not isinstance(e, Resource):
            continue
        if bool(getattr(e, "consumed", False)):
            continue

        pos = world.grid.wrap(e.position)
        d = int(world.grid.distance(origin, pos))
        if d <= sense_range:
            sensed.append((d, str(e.id), e))

    sensed.sort(key=lambda t: (t[0], t[1]))
    return [r for (_, __, r) in sensed]


def sense_nearby(organism: Organism, world: WorldState) -> list[Resource]:
    """Backwards-compatible alias for :func:`sense_nearby_resources`.

    Kept to satisfy external imports expecting `sense_nearby`.
    """

    return sense_nearby_resources(organism, world)
