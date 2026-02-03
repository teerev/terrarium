from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities import Entity, EntityType, generate_id
from terrarium.world.grid import Position


@dataclass
class DummyEntity:
    id: object
    position: Position
    entity_type: EntityType


def test_entity_protocol_attributes() -> None:
    e = DummyEntity(id=generate_id(), position=Position(1, 2), entity_type=EntityType.ORGANISM)

    # Protocol should be satisfied structurally at runtime.
    assert isinstance(e, Entity)

    # Position must be gettable and settable.
    e.position = Position(3, 4)
    assert e.position == Position(3, 4)


def test_entity_id_unique() -> None:
    a = generate_id()
    b = generate_id()
    assert a != b


def test_entity_type_enum() -> None:
    assert EntityType.ORGANISM.value == "organism"
    assert EntityType.RESOURCE.value == "resource"
