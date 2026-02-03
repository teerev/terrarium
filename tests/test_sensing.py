from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.sensing import sense_nearby_resources
from terrarium.entities.resource import create_resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class _Pheno:
    sense_range: int


@dataclass(slots=True)
class _Org:
    id: str
    position: Position
    phenotype: _Pheno


def test_sense_nearby_resources_within_range_sorted_by_distance() -> None:
    world = WorldState(Grid(10, 10), seed=1)

    org = _Org(id="org", position=Position(0, 0), phenotype=_Pheno(sense_range=2))
    world.add_entity(org)

    r1 = create_resource(Position(1, 0), 1, id="r1")  # distance 1
    r2 = create_resource(Position(2, 0), 1, id="r2")  # distance 2
    r3 = create_resource(Position(3, 0), 1, id="r3")  # distance 3 (out of range)
    world.add_entity(r1)
    world.add_entity(r2)
    world.add_entity(r3)

    sensed = sense_nearby_resources(org, world)
    assert [str(r.id) for r in sensed] == ["r1", "r2"]


def test_sense_nearby_resources_zero_range_returns_empty() -> None:
    world = WorldState(Grid(10, 10), seed=1)

    org = _Org(id="org", position=Position(0, 0), phenotype=_Pheno(sense_range=0))
    world.add_entity(org)

    world.add_entity(create_resource(Position(1, 0), 1, id="r1"))

    assert sense_nearby_resources(org, world) == []
