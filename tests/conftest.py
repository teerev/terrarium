"""Shared pytest fixtures for terrarium.

Keep fixtures small and composable. Prefer using built-in pytest fixtures
(e.g., tmp_path) and layering project-specific helpers on top.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def workdir(tmp_path):
    """Provide an isolated temporary working directory for tests."""

    return tmp_path
