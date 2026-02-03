from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Tuple

from terrarium.io.replay_schema import ReplayFrame, ReplaySchema, validate_replay


class ReplayReader:
    """Read-only replay file reader.

    Supports:
    - Loading + schema validation
    - Frame-by-frame iteration
    - Seeking to a specific tick
    - Computing world state at any tick from initial snapshot + events

    Notes
    -----
    - This reader treats replay events as dict-like payloads and applies a
      conservative best-effort set of event types emitted by this codebase.
    - Unknown events are ignored for state reconstruction, but still available
      in frames.
    """

    def __init__(self, path: str | Path):
        self._path = Path(path)
        if not self._path.exists():
            raise FileNotFoundError(str(self._path))

        with self._path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate file on open.
        validate_replay(data)
        self._replay = ReplaySchema.model_validate(data)

        self._frames: List[ReplayFrame] = list(self._replay.frames)
        self._tick_to_frame_index: Dict[int, int] = {
            int(fr.tick): i for i, fr in enumerate(self._frames)
        }

        self._start_tick = int(self._replay.header.start_tick)
        self._end_tick = int(self._replay.header.end_tick)

        # Cache reconstructed states for random access.
        # Keyed by tick.
        self._state_cache: Dict[int, Dict[str, Any]] = {
            self._start_tick: self._deepcopy_jsonable(self._replay.initial_snapshot)
        }

    @property
    def tick_range(self) -> Tuple[int, int]:
        return (int(self._start_tick), int(self._end_tick))

    def __iter__(self) -> Iterator[ReplayFrame]:
        # Yield frames in chronological order.
        yield from self._frames

    def get_frame(self, tick: int) -> Dict[str, Any]:
        """Return the reconstructed world state at *tick*.

        The returned object is a JSON-serializable dict matching the snapshot
        structure produced by terrarium.io.snapshot.
        """

        t = int(tick)
        if t < self._start_tick or t > self._end_tick:
            raise ValueError(
                f"tick {t} out of range [{self._start_tick}, {self._end_tick}]"
            )

        cached = self._state_cache.get(t)
        if cached is not None:
            return self._deepcopy_jsonable(cached)

        # Find best base tick from cache <= t.
        base_tick = max(k for k in self._state_cache.keys() if k <= t)
        state = self._deepcopy_jsonable(self._state_cache[base_tick])

        # Apply frames from base_tick+1 .. t (inclusive).
        for frame_tick in self._frame_ticks_in_range(base_tick + 1, t):
            idx = self._tick_to_frame_index.get(frame_tick)
            if idx is None:
                # No events for this tick.
                self._apply_tick_advance(state, frame_tick)
                self._state_cache[frame_tick] = self._deepcopy_jsonable(state)
                continue

            frame = self._frames[idx]
            self._apply_events(state, int(frame.tick), frame.events)
            self._state_cache[int(frame.tick)] = self._deepcopy_jsonable(state)

        # If there were no frames exactly at tick, ensure the tick is cached by
        # advancing to it.
        if t not in self._state_cache:
            self._apply_tick_advance(state, t)
            self._state_cache[t] = self._deepcopy_jsonable(state)

        return self._deepcopy_jsonable(self._state_cache[t])

    def _frame_ticks_in_range(self, start: int, end: int) -> List[int]:
        if start > end:
            return []
        # Frames are already ordered; collect relevant ticks.
        out: List[int] = []
        for fr in self._frames:
            ft = int(fr.tick)
            if ft < start:
                continue
            if ft > end:
                break
            out.append(ft)
        # Also include ticks in gaps where there are no frames, because tick
        # advancement matters for world.tick.
        # We keep it cheap by only filling gaps when needed in get_frame, but
        # we still need to include the target tick if it's not a frame.
        if not out:
            return [end]
        if out[-1] != end:
            out.append(end)
        return out

    @staticmethod
    def _deepcopy_jsonable(obj: Any) -> Any:
        # Minimal deep copy for dict/list primitives.
        if isinstance(obj, dict):
            return {k: ReplayReader._deepcopy_jsonable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [ReplayReader._deepcopy_jsonable(v) for v in obj]
        return obj

    def _apply_tick_advance(self, state: Dict[str, Any], tick: int) -> None:
        # Snapshot dict uses "tick" as integer.
        state["tick"] = int(tick)

    def _apply_events(self, state: Dict[str, Any], tick: int, events: List[Any]) -> None:
        # Advance tick first.
        self._apply_tick_advance(state, tick)

        for ev in events:
            # Pydantic ReplayEvent is a BaseModel with dict-like access.
            if hasattr(ev, "model_dump"):
                d = ev.model_dump()
            elif isinstance(ev, Mapping):
                d = dict(ev)
            else:
                continue

            event_type = str(d.get("event_type", ""))

            if event_type == "birth":
                self._apply_birth(state, d)
            elif event_type == "death":
                self._apply_death(state, d)
            elif event_type == "movement":
                self._apply_movement(state, d)
            elif event_type == "resource_spawn":
                self._apply_resource_spawn(state, d)
            elif event_type == "consumption":
                self._apply_consumption(state, d)
            else:
                # Unknown event types are ignored for reconstruction.
                continue

    @staticmethod
    def _entities_list(state: Dict[str, Any]) -> List[Dict[str, Any]]:
        ents = state.get("entities")
        if not isinstance(ents, list):
            ents = []
            state["entities"] = ents
        # Ensure elements are dicts.
        out: List[Dict[str, Any]] = []
        for e in ents:
            if isinstance(e, dict):
                out.append(e)
        if len(out) != len(ents):
            state["entities"] = out
        return out

    @staticmethod
    def _find_entity_index(entities: List[Dict[str, Any]], entity_id: str) -> int | None:
        for i, e in enumerate(entities):
            if str(e.get("id")) == entity_id:
                return i
        return None

    def _apply_birth(self, state: Dict[str, Any], ev: Mapping[str, Any]) -> None:
        entities = self._entities_list(state)
        payload = ev.get("payload")
        if not isinstance(payload, Mapping):
            payload = ev

        oid = payload.get("organism_id") or payload.get("id")
        if oid is None:
            return
        oid_s = str(oid)

        pos = payload.get("position")
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            position = [int(pos[0]), int(pos[1])]
        else:
            position = [0, 0]

        energy = payload.get("energy")
        if energy is None:
            energy = payload.get("initial_energy")
        if energy is None:
            energy = 0

        ent = {
            "id": oid_s,
            "type": "organism",
            "position": position,
            "energy": int(energy),
            "age": 0,
        }

        idx = self._find_entity_index(entities, oid_s)
        if idx is None:
            entities.append(ent)
        else:
            entities[idx] = ent

    def _apply_death(self, state: Dict[str, Any], ev: Mapping[str, Any]) -> None:
        entities = self._entities_list(state)
        payload = ev.get("payload")
        if not isinstance(payload, Mapping):
            payload = ev

        oid = payload.get("organism_id") or payload.get("entity_id") or payload.get("id")
        if oid is None:
            return
        oid_s = str(oid)

        idx = self._find_entity_index(entities, oid_s)
        if idx is not None:
            entities.pop(idx)

    def _apply_movement(self, state: Dict[str, Any], ev: Mapping[str, Any]) -> None:
        entities = self._entities_list(state)
        payload = ev.get("payload")
        if not isinstance(payload, Mapping):
            payload = ev

        eid = payload.get("organism_id") or payload.get("entity_id") or payload.get("id")
        if eid is None:
            return
        eid_s = str(eid)

        pos = payload.get("to") or payload.get("position")
        if not (isinstance(pos, (list, tuple)) and len(pos) == 2):
            return
        new_pos = [int(pos[0]), int(pos[1])]

        idx = self._find_entity_index(entities, eid_s)
        if idx is None:
            return
        entities[idx]["position"] = new_pos

    def _apply_resource_spawn(self, state: Dict[str, Any], ev: Mapping[str, Any]) -> None:
        entities = self._entities_list(state)
        payload = ev.get("payload")
        if not isinstance(payload, Mapping):
            payload = ev

        rid = payload.get("resource_id") or payload.get("id")
        if rid is None:
            return
        rid_s = str(rid)

        pos = payload.get("position")
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            position = [int(pos[0]), int(pos[1])]
        else:
            position = [0, 0]

        energy_value = payload.get("energy_value")
        if energy_value is None:
            energy_value = payload.get("energy")
        if energy_value is None:
            energy_value = 1

        ent = {
            "id": rid_s,
            "type": "resource",
            "position": position,
            "energy_value": int(energy_value),
            "consumed": False,
        }

        idx = self._find_entity_index(entities, rid_s)
        if idx is None:
            entities.append(ent)
        else:
            entities[idx] = ent

    def _apply_consumption(self, state: Dict[str, Any], ev: Mapping[str, Any]) -> None:
        entities = self._entities_list(state)
        payload = ev.get("payload")
        if not isinstance(payload, Mapping):
            payload = ev

        rid = payload.get("resource_id")
        if rid is not None:
            rid_s = str(rid)
            idx = self._find_entity_index(entities, rid_s)
            if idx is not None:
                # Either remove or mark consumed. Use mark consumed to keep id stable.
                entities[idx]["consumed"] = True

        oid = payload.get("organism_id")
        if oid is not None:
            oid_s = str(oid)
            idx2 = self._find_entity_index(entities, oid_s)
            if idx2 is not None:
                delta = payload.get("energy_gained")
                if delta is None:
                    delta = payload.get("amount")
                if delta is None:
                    return
                try:
                    entities[idx2]["energy"] = int(entities[idx2].get("energy", 0)) + int(delta)
                except Exception:
                    return
