from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping

from terrarium.engine.rng import Rng, SeededRNG
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


SCHEMA_VERSION = 1


def _position_to_jsonable(pos: Position) -> list[int]:
    return [int(pos.x), int(pos.y)]


def _position_from_jsonable(payload: Any) -> Position:
    if (
        not isinstance(payload, (list, tuple))
        or len(payload) != 2
    ):
        raise ValueError("Invalid position payload")
    return Position(int(payload[0]), int(payload[1]))


def _rng_state_to_jsonable(state: Rng) -> list[Any]:
    version, internal, gauss = state
    return [
        version,
        [list(t) if isinstance(t, tuple) else t for t in internal],
        gauss,
    ]


def _rng_state_from_jsonable(payload: Any) -> Rng:
    if not isinstance(payload, (list, tuple)) or len(payload) != 3:
        raise ValueError("Invalid RNG state payload")
    version, internal, gauss = payload
    internal_t = tuple(tuple(t) if isinstance(t, list) else t for t in internal)
    return (version, internal_t, gauss)


def _organism_to_dict(o: Organism) -> dict[str, Any]:
    # Note: Organism.age is mutable and important for exact resumption.
    return {
        "id": str(o.id),
        "position": _position_to_jsonable(o.position),
        "energy": int(o.energy),
        "age": int(o.age),
        "genome": o.genome.to_dict(),
        "lineage": {
            "parent_id": str(o.parent_id) if o.parent_id is not None else None,
            "lineage_id": str(o.lineage_id),
            "generation": int(o.generation),
            "birth_tick": int(o.birth_tick),
        },
    }


def _resource_to_dict(r: Resource) -> dict[str, Any]:
    return {
        "id": str(r.id) if r.id is not None else None,
        "position": _position_to_jsonable(r.position),
        "energy_value": int(r.energy_value),
        "consumed": bool(r.consumed),
    }


@dataclass(frozen=True, slots=True)
class WorldSnapshot:
    """JSON-serializable snapshot of a world.

    This captures everything required to resume simulation deterministically:
    - schema/version and metadata
    - tick and grid configuration
    - full entity state (organisms + resources)
    - RNG seed and internal state

    Note: this object is in-memory only; file I/O is out of scope.
    """

    schema_version: int
    timestamp: str

    tick: int
    grid: dict[str, int]

    rng_seed: int
    rng_state: list[Any]

    organisms: list[dict[str, Any]]
    resources: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": int(self.schema_version),
            "timestamp": str(self.timestamp),
            "tick": int(self.tick),
            "grid": {"width": int(self.grid["width"]), "height": int(self.grid["height"])},
            "rng": {"seed": int(self.rng_seed), "state": self.rng_state},
            "organisms": list(self.organisms),
            "resources": list(self.resources),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "WorldSnapshot":
        schema_version = int(d.get("schema_version", 0))
        if schema_version != SCHEMA_VERSION:
            raise ValueError(f"Unsupported snapshot schema_version: {schema_version}")

        grid = d.get("grid")
        rng = d.get("rng")
        if not isinstance(grid, Mapping) or not isinstance(rng, Mapping):
            raise ValueError("Invalid snapshot payload")

        return cls(
            schema_version=schema_version,
            timestamp=str(d.get("timestamp", "")),
            tick=int(d.get("tick", 0)),
            grid={"width": int(grid.get("width")), "height": int(grid.get("height"))},
            rng_seed=int(rng.get("seed")),
            rng_state=list(rng.get("state")),
            organisms=list(d.get("organisms", [])),
            resources=list(d.get("resources", [])),
        )


def create_snapshot(world: WorldState, rng: SeededRNG) -> WorldSnapshot:
    """Capture a complete snapshot of the given world and RNG."""

    entities = list(world._entities.values())  # type: ignore[attr-defined]
    organisms: list[dict[str, Any]] = []
    resources: list[dict[str, Any]] = []

    for ent in entities:
        if isinstance(ent, Organism):
            organisms.append(_organism_to_dict(ent))
        elif isinstance(ent, Resource):
            resources.append(_resource_to_dict(ent))

    # Stable ordering for deterministic output
    organisms.sort(key=lambda x: str(x.get("id", "")))
    resources.sort(key=lambda x: str(x.get("id", "")))

    ts = datetime.now(timezone.utc).isoformat()

    return WorldSnapshot(
        schema_version=SCHEMA_VERSION,
        timestamp=ts,
        tick=int(world.tick),
        grid={"width": int(world.grid.width), "height": int(world.grid.height)},
        rng_seed=int(rng.seed),
        rng_state=_rng_state_to_jsonable(rng.get_state()),
        organisms=organisms,
        resources=resources,
    )


def restore_snapshot(snapshot: WorldSnapshot | Mapping[str, Any]) -> tuple[WorldState, SeededRNG]:
    """Restore a world and RNG from a snapshot."""

    snap = snapshot if isinstance(snapshot, WorldSnapshot) else WorldSnapshot.from_dict(snapshot)

    grid = Grid(int(snap.grid["width"]), int(snap.grid["height"]))

    world = WorldState(grid, seed=int(snap.rng_seed))
    rng = SeededRNG(int(snap.rng_seed))
    rng.set_state(_rng_state_from_jsonable(snap.rng_state))

    # Restore tick exactly
    world._tick = int(snap.tick)  # type: ignore[attr-defined]

    # Restore entities
    for o in snap.organisms:
        if not isinstance(o, Mapping):
            raise ValueError("Invalid organism payload")
        lineage = o.get("lineage")
        if not isinstance(lineage, Mapping):
            raise ValueError("Invalid organism lineage payload")

        org = Organism(
            position=_position_from_jsonable(o.get("position")),
            energy=int(o.get("energy")),
            id=o.get("id"),
            genome=Genome.from_dict(o.get("genome", {})),
            parent_id=lineage.get("parent_id"),
            lineage_id=lineage.get("lineage_id"),
            generation=int(lineage.get("generation")),
            birth_tick=int(lineage.get("birth_tick")),
        )
        # Age is not settable via constructor; set internal field for exact restore.
        org._age = int(o.get("age", 0))  # type: ignore[attr-defined]
        world.add_entity(org)

    for r in snap.resources:
        if not isinstance(r, Mapping):
            raise ValueError("Invalid resource payload")

        res = Resource(
            position=_position_from_jsonable(r.get("position")),
            energy_value=int(r.get("energy_value")),
            id=r.get("id"),
            consumed=bool(r.get("consumed", False)),
        )
        world.add_entity(res)

    return world, rng
