"""Terrarium simulation package.

This package provides the top-level namespace and re-exports key subpackages.
"""

from __future__ import annotations

from . import core, engine, entities, world

__all__ = ["__version__", "core", "world", "entities", "engine"]

__version__ = "0.1.0"
