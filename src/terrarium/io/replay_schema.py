from __future__ import annotations

"""Replay JSON schema models.

This module formalizes the Terrarium replay file format for interoperability.

Design goals
------------
- JSON Schema compatible (exportable via Pydantic's `model_json_schema`).
- Efficient parsing: events are grouped by tick (frames), avoiding deeply nested
  structures and allowing fast frame-by-frame rendering.
- Compact positions: `[x, y]` arrays.

Public API
----------
- ReplaySchema: root Pydantic model for replay documents
- validate_replay(data) -> bool: schema validation helper

Schema overview
---------------
Replay document (top-level):
- kind: "terrarium.replay"
- format_version: integer (currently 1)
- header: metadata about the simulation/run
- initial_snapshot: a WorldSnapshot dict (as produced by terrarium.io.snapshot)
- frames: list of frames, each containing events for a tick

Notes
-----
- The exact contents of events are intentionally flexible for forward
  compatibility. Events are required to have at least `event_type` and `tick`.
- `initial_snapshot` is treated as an opaque JSON object here; it is defined by
  terrarium.io.snapshot and includes its own `schema_version`.
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ReplayHeader(BaseModel):
    """Replay metadata.

    Fields are intentionally simple, stable, and JSON-friendly.
    """

    model_config = ConfigDict(extra="forbid")

    seed: Optional[int] = None
    config: Any = None
    duration_ticks: int = 0
    start_tick: int = 0
    end_tick: int = 0
    grid: Dict[str, int] = Field(default_factory=dict)


class ReplayEvent(BaseModel):
    """A single simulation event.

    Minimum contract:
    - event_type: stable event name
    - tick: integer tick when the event occurred

    Additional keys are allowed to support multiple event variants.
    """

    model_config = ConfigDict(extra="allow")

    event_type: str
    tick: int


class ReplayFrame(BaseModel):
    """Events grouped by tick for efficient rendering."""

    model_config = ConfigDict(extra="forbid")

    tick: int
    events: List[ReplayEvent] = Field(default_factory=list)


class ReplaySchema(BaseModel):
    """Root schema model for replay JSON files."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["terrarium.replay"] = "terrarium.replay"
    format_version: Literal[1] = 1

    header: ReplayHeader

    # Snapshot schema is defined elsewhere; we keep it opaque but require object.
    initial_snapshot: Dict[str, Any]

    # Tick-grouped events.
    frames: List[ReplayFrame] = Field(default_factory=list)


def validate_replay(data: Any) -> bool:
    """Validate *data* against ReplaySchema.

    Returns True if valid, otherwise raises pydantic.ValidationError.
    """

    ReplaySchema.model_validate(data)
    return True
