from __future__ import annotations

import importlib


def test_subpackages_importable() -> None:
    import terrarium

    # Ensure the top-level re-exports allow these imports.
    assert terrarium.core is not None
    assert terrarium.world is not None
    assert terrarium.entities is not None
    assert terrarium.engine is not None

    importlib.import_module("terrarium.core")
    importlib.import_module("terrarium.world")
    importlib.import_module("terrarium.entities")
    importlib.import_module("terrarium.engine")


def test_module_docstrings() -> None:
    import terrarium

    assert terrarium.__doc__ is not None and terrarium.__doc__.strip() != ""

    for name in ("core", "world", "entities", "engine"):
        mod = importlib.import_module(f"terrarium.{name}")
        assert mod.__doc__ is not None and mod.__doc__.strip() != ""


def test_subpackage_public_exports_present() -> None:
    """Basic smoke test for the intended public exports from each subpackage."""

    from terrarium import core, engine, entities, world

    # core
    assert core.EntityId is not None
    assert core.Position is not None
    assert core.RandomSource is not None

    # world
    assert world.Grid is not None
    assert world.WorldState is not None

    # entities
    assert entities.Entity is not None
    assert entities.Organism is not None
    assert entities.Resource is not None

    # engine
    assert engine.DefaultRandom is not None
    assert engine.SimulationEngine is not None
