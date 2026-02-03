from __future__ import annotations

import importlib


def test_subpackages_importable() -> None:
    import terrarium

    assert terrarium.core is not None
    assert terrarium.world is not None
    assert terrarium.entities is not None
    assert terrarium.engine is not None

    # Ensure import by module path also works
    assert importlib.import_module("terrarium.core") is not None
    assert importlib.import_module("terrarium.world") is not None
    assert importlib.import_module("terrarium.entities") is not None
    assert importlib.import_module("terrarium.engine") is not None


def test_subpackage_init_has_docstring() -> None:
    core = importlib.import_module("terrarium.core")
    world = importlib.import_module("terrarium.world")
    entities = importlib.import_module("terrarium.entities")
    engine = importlib.import_module("terrarium.engine")

    assert isinstance(core.__doc__, str) and core.__doc__.strip()
    assert isinstance(world.__doc__, str) and world.__doc__.strip()
    assert isinstance(entities.__doc__, str) and entities.__doc__.strip()
    assert isinstance(engine.__doc__, str) and engine.__doc__.strip()
