from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from terrarium.io.snapshot import WorldSnapshot


FILE_FORMAT_VERSION = 1


class PersistenceError(RuntimeError):
    """Raised for file I/O or format problems when saving/loading snapshots."""


def _ensure_supported_extension(path: Path) -> None:
    suffix = path.suffix.lower()
    if suffix not in {".terrarium", ".json"}:
        raise ValueError("Unsupported file extension; use .terrarium or .json")


def save_snapshot(snapshot: WorldSnapshot | Mapping[str, Any], path: str | Path) -> None:
    """Save a snapshot to disk as human-readable JSON.

    Writes atomically: write to a temp file in the same directory then replace.

    Parameters
    ----------
    snapshot:
        A WorldSnapshot or a dict payload compatible with WorldSnapshot.from_dict.
    path:
        Destination path. Must end with .terrarium or .json.
    """

    out_path = Path(path)
    _ensure_supported_extension(out_path)

    snap = snapshot if isinstance(snapshot, WorldSnapshot) else WorldSnapshot.from_dict(snapshot)

    payload = {
        "file_format": {"name": "terrarium-snapshot", "version": int(FILE_FORMAT_VERSION)},
        "snapshot": snap.to_dict(),
    }

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = out_path.with_name(out_path.name + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
            f.write("\n")
        tmp_path.replace(out_path)
    except OSError as e:
        raise PersistenceError(f"Failed to save snapshot to '{out_path}': {e}") from e


def load_snapshot(path: str | Path) -> WorldSnapshot:
    """Load a snapshot from disk.

    Parameters
    ----------
    path:
        Source path. Must end with .terrarium or .json.

    Returns
    -------
    WorldSnapshot

    Raises
    ------
    PersistenceError
        For file I/O errors or invalid JSON.
    ValueError
        For unsupported schema/file versions or invalid snapshot payload.
    """

    in_path = Path(path)
    _ensure_supported_extension(in_path)

    try:
        with in_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError as e:
        raise PersistenceError(f"Snapshot file not found: '{in_path}'") from e
    except json.JSONDecodeError as e:
        raise PersistenceError(f"Invalid JSON in snapshot file '{in_path}': {e}") from e
    except OSError as e:
        raise PersistenceError(f"Failed to read snapshot file '{in_path}': {e}") from e

    if not isinstance(payload, Mapping):
        raise ValueError("Invalid snapshot file payload")

    ff = payload.get("file_format")
    if not isinstance(ff, Mapping):
        raise ValueError("Missing file_format header")

    if str(ff.get("name")) != "terrarium-snapshot":
        raise ValueError("Unrecognized snapshot file format")

    version = int(ff.get("version", 0))
    if version != FILE_FORMAT_VERSION:
        raise ValueError(f"Unsupported snapshot file format version: {version}")

    snap_payload = payload.get("snapshot")
    if not isinstance(snap_payload, Mapping):
        raise ValueError("Missing snapshot payload")

    return WorldSnapshot.from_dict(snap_payload)
