# Terrarium Replay JSON Format (v1)

This document specifies the Terrarium replay JSON format used for exporting simulation runs for external visualization tools.

## Design goals

- JSON Schema compatible.
- Efficient parsing and rendering: events are grouped by tick (`frames`).
- Compact positions: `[x, y]` integer arrays.
- Forward-compatible event payloads: events require only `event_type` and `tick`; additional keys are allowed.

## Top-level structure

A replay document is a single JSON object:

- `kind` (string): must be `"terrarium.replay"`.
- `format_version` (int): must be `1`.
- `header` (object): simulation metadata (see below).
- `initial_snapshot` (object): a `WorldSnapshot` dict as produced by `terrarium.io.snapshot`.
- `frames` (array): list of frames; each frame contains all events for a given tick.

### Header

`header` is an object with:

- `seed` (int|null): RNG seed.
- `config` (any): optional simulation config payload (exported best-effort).
- `duration_ticks` (int): `end_tick - start_tick`.
- `start_tick` (int): snapshot tick at export time.
- `end_tick` (int): simulation tick value used as the end marker.
- `grid` (object): `{ "width": int, "height": int }`.

### Frames and events

`frames` is an array of objects, each:

- `tick` (int): the tick for this frame.
- `events` (array): events that occurred at that tick.

Each event is an object with required fields:

- `event_type` (string): stable event name.
- `tick` (int): tick when the event occurred.

Additional keys are allowed for event-specific payloads.

## JSON Schema

The authoritative schema models live in `terrarium.io.replay_schema` and are exportable as JSON Schema via Pydantic:

- `ReplaySchema.model_json_schema()`

Validation helper:

- `terrarium.io.validate_replay(data) -> bool`

## Example

See: `examples/replay.example.v1.json`.
