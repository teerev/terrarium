from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from terrarium.io.replay_schema import ReplaySchema
from terrarium.io.snapshot import create_snapshot


@dataclass(frozen=True, slots=True)
class ReplayFormat:
    """Constants for the Terrarium replay export format."""

    version: int = 1
    kind: str = "terrarium.replay"


def _config_to_jsonable(config: Any) -> Any:
    """Best-effort conversion of a simulation config to a JSON-able payload."""

    if config is None:
        return None

    # Many configs in this repo are plain dicts or dataclasses.
    if isinstance(config, Mapping):
        return dict(config)

    to_dict = getattr(config, "to_dict", None)
    if callable(to_dict):
        try:
            payload = to_dict()
            if isinstance(payload, Mapping):
                return dict(payload)
            return payload
        except Exception:
            pass

    # Dataclass-like
    try:
        from dataclasses import asdict, is_dataclass

        if is_dataclass(config):
            return asdict(config)
    except Exception:
        pass

    # Fallback: use __dict__ if present, else string repr.
    d = getattr(config, "__dict__", None)
    if isinstance(d, dict):
        return dict(d)

    return str(config)


def export_replay(sim: Any, path: str | Path) -> None:
    """Export a self-contained replay file for external visualization.

    The exported JSON includes:
    - format metadata (kind/version)
    - simulation metadata (seed/config/duration/tick range/grid dimensions)
    - initial snapshot (WorldSnapshot dict)
    - events grouped by tick into frames for efficient playback

    Export validates the produced payload against `ReplaySchema`.

    Parameters
    ----------
    sim:
        A simulation-like object. Expected to expose:
        - world (WorldState)
        - rng (SeededRNG) or world.rng
        - events (iterable) or event_log/events_log (iterable)
        - config (optional)
    path:
        Output file path.
    """

    out_path = Path(path)

    world = getattr(sim, "world", None)
    if world is None:
        raise ValueError("export_replay expects sim.world")

    rng = getattr(sim, "rng", None)
    if rng is None:
        rng = getattr(world, "rng", None)
    if rng is None:
        raise ValueError("export_replay expects sim.rng or sim.world.rng")

    # Initial snapshot at time of export.
    snapshot = create_snapshot(world, rng).to_dict()

    grid = snapshot.get("grid") or {}

    # Get config/seed/duration/ticks best-effort.
    seed = None
    if isinstance(snapshot.get("rng"), Mapping):
        seed = snapshot["rng"].get("seed")

    config = _config_to_jsonable(getattr(sim, "config", None))

    start_tick = int(snapshot.get("tick", 0))
    end_tick = int(getattr(sim, "tick", start_tick))
    duration_ticks = int(max(0, end_tick - start_tick))

    # Find an event log attribute.
    events_obj = None
    for name in ("events", "event_log", "events_log"):
        if hasattr(sim, name):
            events_obj = getattr(sim, name)
            break

    events: list[dict[str, Any]] = []
    if events_obj is not None:
        try:
            for e in list(events_obj):
                to_dict = getattr(e, "to_dict", None)
                if callable(to_dict):
                    events.append(to_dict())
                elif isinstance(e, Mapping):
                    events.append(dict(e))
                else:
                    # Unknown event type; best-effort serialize.
                    events.append(
                        {
                            "event_type": str(getattr(e, "event_type", "event")),
                            "tick": int(getattr(e, "tick", 0)),
                            "payload": str(e),
                        }
                    )
        except TypeError:
            # Non-iterable events container; ignore.
            events = []

    # Enforce chronological ordering.
    events.sort(key=lambda d: int(d.get("tick", 0)))

    # Group events into frames by tick.
    frames: list[dict[str, Any]] = []
    current_tick: int | None = None
    current_events: list[dict[str, Any]] = []
    for e in events:
        t = int(e.get("tick", 0))
        if current_tick is None:
            current_tick = t
            current_events = [e]
            continue
        if t != current_tick:
            frames.append({"tick": int(current_tick), "events": list(current_events)})
            current_tick = t
            current_events = [e]
        else:
            current_events.append(e)

    if current_tick is not None:
        frames.append({"tick": int(current_tick), "events": list(current_events)})

    payload: dict[str, Any] = {
        "kind": ReplayFormat().kind,
        "format_version": ReplayFormat().version,
        "header": {
            "seed": int(seed) if seed is not None else None,
            "config": config,
            "duration_ticks": duration_ticks,
            "start_tick": int(start_tick),
            "end_tick": int(end_tick),
            "grid": {
                "width": int(grid.get("width", 0)) if isinstance(grid, Mapping) else 0,
                "height": int(grid.get("height", 0)) if isinstance(grid, Mapping) else 0,
            },
        },
        "initial_snapshot": snapshot,
        "frames": frames,
    }

    # Validate on export (raises on failure).
    ReplaySchema.model_validate(payload)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
