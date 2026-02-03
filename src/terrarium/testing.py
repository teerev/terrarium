from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from terrarium.engine.simulator import Simulator
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.io.snapshot import WorldSnapshot, create_snapshot, restore_snapshot
from terrarium.world.state import WorldState


def snapshot_world_state(world: WorldState) -> dict[str, Any]:
    """Return a deterministic, deep-ish snapshot of the world's state.

    Snapshot is designed for test comparisons and includes:
    - tick
    - grid dimensions
    - entity list with stable ordering and key state for known entity types
    """

    entities = list(world._entities.values())  # type: ignore[attr-defined]

    def ent_key(e: Any) -> str:
        return str(getattr(e, "id", ""))

    items: list[dict[str, Any]] = []
    for ent in sorted(entities, key=ent_key):
        base: dict[str, Any] = {
            "id": str(getattr(ent, "id")),
            "type": str(getattr(ent, "entity_type", type(ent).__name__)),
            "position": (
                int(getattr(getattr(ent, "position"), "x")),
                int(getattr(getattr(ent, "position"), "y")),
            ),
        }

        if isinstance(ent, Organism):
            base.update({"energy": int(ent.energy), "age": int(ent.age)})
        elif isinstance(ent, Resource):
            base.update({"energy_value": int(ent.energy_value), "consumed": bool(ent.consumed)})

        items.append(base)

    return {
        "tick": int(world.tick),
        "grid": {"width": int(world.grid.width), "height": int(world.grid.height)},
        "entities": items,
    }


@dataclass(frozen=True, slots=True)
class ReplayResult:
    ok: bool


def verify_replay(snapshot: WorldSnapshot | dict[str, Any], n_steps: int) -> ReplayResult:
    """Verify deterministic replay from a snapshot.

    Runs the simulation twice from the same snapshot for *n_steps* and compares
    the resulting snapshots.

    Notes
    -----
    - This intentionally does not compare event logs.
    - Comparison is done via snapshot dicts (excluding timestamp).
    """

    steps = int(n_steps)
    if steps < 0:
        raise ValueError("n_steps must be non-negative")

    def run_once() -> dict[str, Any]:
        world, rng = restore_snapshot(snapshot)
        sim = Simulator(world, rng)
        for _ in range(steps):
            sim.step()
        out = create_snapshot(world, rng).to_dict()
        # Timestamp is expected to differ.
        out.pop("timestamp", None)
        return out

    a = run_once()
    b = run_once()

    return ReplayResult(ok=(a == b))
