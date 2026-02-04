"""Terrarium simulation package.

This top-level package exposes the primary internal subpackages:
- terrarium.core
- terrarium.world
- terrarium.entities
- terrarium.engine
"""

from __future__ import annotations

from terrarium import core, engine, entities, world

__all__ = ["__version__", "core", "world", "entities", "engine"]

__version__: str = "0.1.0"
