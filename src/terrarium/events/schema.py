from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from terrarium.core import EntityId, Position


class Event(Protocol):
    """Base protocol for all observable simulation events."""

    tick: int
    event_type: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the event."""


@dataclass(frozen=True, slots=True)
class BirthEvent:
    tick: int
    parent_id: EntityId
    offspring_id: EntityId
    genome: Mapping[str, Any]
    position: Position

    event_type: str = "birth"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "tick": int(self.tick),
            "parent_id": str(self.parent_id),
            "offspring_id": str(self.offspring_id),
            "genome": dict(self.genome),
            "position": (int(self.position[0]), int(self.position[1])),
        }


@dataclass(frozen=True, slots=True)
class DeathEvent:
    tick: int
    organism_id: EntityId
    cause: str
    final_energy: int

    event_type: str = "death"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "tick": int(self.tick),
            "organism_id": str(self.organism_id),
            "cause": str(self.cause),
            "final_energy": int(self.final_energy),
        }


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    tick: int
    organism_id: EntityId
    resource_id: EntityId
    energy_gained: int

    event_type: str = "consumption"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "tick": int(self.tick),
            "organism_id": str(self.organism_id),
            "resource_id": str(self.resource_id),
            "energy_gained": int(self.energy_gained),
        }


@dataclass(frozen=True, slots=True)
class MovementEvent:
    tick: int
    organism_id: EntityId
    from_position: Position
    to_position: Position

    event_type: str = "movement"

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "tick": int(self.tick),
            "organism_id": str(self.organism_id),
            "from_position": (
                int(self.from_position[0]),
                int(self.from_position[1]),
            ),
            "to_position": (int(self.to_position[0]), int(self.to_position[1])),
        }
