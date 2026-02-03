from __future__ import annotations

from dataclasses import dataclass

from terrarium.entities.base import Entity, EntityType, generate_id
from terrarium.world.grid import Position


def test_generate_id_unique() -> None:
    ids = {generate_id() for _ in range(200)}
    assert len(ids) == 200


def test_entity_protocol_structural() -> None:
    @dataclass
    class Dummy:
        _id: object
        _position: Position

        @property
        def id(self):
            return self._id

        @property
        def position(self) -> Position:
            return self._position

        @position.setter
        def position(self, value: Position) -> None:
            self._position = value

        @property
        def entity_type(self) -> EntityType:
            return EntityType.ORGANISM

    d = Dummy(generate_id(), Position(1, 2))
    e: Entity = d
    assert e.entity_type in (EntityType.ORGANISM, EntityType.RESOURCE)
    assert e.position == Position(1, 2)
    e.position = Position(3, 4)
    assert e.position == Position(3, 4)
