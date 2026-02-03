"""Terrarium package.

This package provides the CLI entrypoint and core simulation code.
"""

from __future__ import annotations

from . import core, engine, entities, world

__all__ = ["__version__", "core", "world", "entities", "engine"]

__version__: str = "0.1.0"
