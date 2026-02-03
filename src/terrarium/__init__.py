"""Terrarium package.

This package provides the public API surface for the terrarium simulation.
Core simulation components are organized into subpackages:
- terrarium.core
- terrarium.world
- terrarium.entities
- terrarium.engine
"""

from __future__ import annotations

__version__ = "0.1.0"

from terrarium import core, engine, entities, world

__all__ = [
    "__version__",
    "core",
    "world",
    "entities",
    "engine",
]
