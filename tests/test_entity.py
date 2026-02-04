from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities import Entity, EntityType, generate_id
from terrarium.world.grid import Position


def test_entity_protocol_attributes() -> None:
    @dataclass
    class Dummy:
        id: object
        position: Position
        entity_type: EntityType

    e: Entity = Dummy(id=generate_id(), position=Position(1, 2), entity_type=EntityType.ORGANISM)

    assert e.entity_type is EntityType.ORGANISM
    e.position = Position(3, 4)
    assert e.position == Position(3, 4)


def test_entity_id_unique() -> None:
    a = generate_id()
    b = generate_id()

    assert a != b
    assert {a, b}  # hashable + usable in sets


def test_entity_type_enum() -> None:
    assert EntityType.ORGANISM.value == "ORGANISM"
    assert EntityType.RESOURCE.value == "RESOURCE"
