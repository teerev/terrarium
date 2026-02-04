from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Protocol

from terrarium.core.types import EntityId, Position


class Event(Protocol):
    """Base protocol for simulation events.

    Design constraints:
    - immutable records (implemented by frozen dataclasses)
    - `tick` timestamp
    - `event_type` discriminator for dispatch/deserialization
    - serializable without information loss via `to_dict()`
    """

    tick: int
    event_type: str

    def to_dict(self) -> Dict[str, Any]:
        ...


def _to_jsonable(obj: Any) -> Any:
    """Convert common Terrarium value types into JSON-friendly structures."""

    if isinstance(obj, tuple):
        return [_to_jsonable(v) for v in obj]

    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]

    # EntityId is a NewType over int; keep as int for lossless JSON
    if isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str) or obj is None:
        return obj

    return obj


@dataclass(frozen=True, slots=True)
class BirthEvent:
    tick: int
    parent_id: EntityId
    offspring_id: EntityId
    genome: Mapping[str, Any]
    position: Position

    event_type: str = "birth"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["parent_id"] = int(self.parent_id)
        d["offspring_id"] = int(self.offspring_id)
        d["position"] = list(self.position)
        d["genome"] = dict(self.genome)
        return _to_jsonable(d)


@dataclass(frozen=True, slots=True)
class DeathEvent:
    tick: int
    organism_id: EntityId
    cause: str
    final_energy: int

    event_type: str = "death"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["organism_id"] = int(self.organism_id)
        d["final_energy"] = int(self.final_energy)
        return _to_jsonable(d)


@dataclass(frozen=True, slots=True)
class ConsumptionEvent:
    tick: int
    organism_id: EntityId
    resource_id: EntityId
    energy_gained: int

    event_type: str = "consumption"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["organism_id"] = int(self.organism_id)
        d["resource_id"] = int(self.resource_id)
        d["energy_gained"] = int(self.energy_gained)
        return _to_jsonable(d)


@dataclass(frozen=True, slots=True)
class MovementEvent:
    tick: int
    organism_id: EntityId
    from_position: Position
    to_position: Position

    event_type: str = "movement"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["organism_id"] = int(self.organism_id)
        d["from_position"] = list(self.from_position)
        d["to_position"] = list(self.to_position)
        return _to_jsonable(d)
