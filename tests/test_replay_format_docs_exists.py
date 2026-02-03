from __future__ import annotations

from pathlib import Path


def test_replay_format_docs_exists(project_root: Path) -> None:
    path = project_root / "docs" / "replay-format.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Terrarium Replay JSON Format" in text
