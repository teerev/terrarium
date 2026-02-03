from __future__ import annotations


def test_public_subpackages_are_importable() -> None:
    # Acceptance command parity: `python -c 'from terrarium import core, world, entities, engine'`
    from terrarium import core, engine, entities, world

    assert core is not None
    assert world is not None
    assert entities is not None
    assert engine is not None
