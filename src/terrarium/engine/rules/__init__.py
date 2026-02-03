"""Engine rules.

Rules are optional, composable components that apply deterministic logic during
simulation steps.
"""

from __future__ import annotations

from .spawning import ResourceSpawner

__all__ = ["ResourceSpawner"]
