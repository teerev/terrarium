from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities import Entity, EntityType, generate_id
from terrarium.world import Position


@dataclass
class DummyEntity:
    _id: object
    _position: Position
    entity_type: EntityType

    @property
    def id(self):
        return self._id

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value


def test_entity_protocol_attributes_and_settable_position():
    e = DummyEntity(_id=generate_id(), _position=Position(1, 2), entity_type=EntityType.ORGANISM)

    # Basic attribute access
    assert e.id is not None
    assert e.position == Position(1, 2)
    assert e.entity_type is EntityType.ORGANISM

    # Position is settable
    e.position = Position(3, 4)
    assert e.position == Position(3, 4)

    # Structural typing: should be runtime-checkable (and useful for tests)
    assert isinstance(e, Entity)


def test_entity_id_unique():
    a = generate_id()
    b = generate_id()
    assert a != b
    assert type(a) is type(b)


def test_entity_type_enum_has_expected_values():
    assert EntityType.ORGANISM.value == "organism"
    assert EntityType.RESOURCE.value == "resource"
