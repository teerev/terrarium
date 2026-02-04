from __future__ import annotations


def test_import_organism_public_api() -> None:
    from terrarium.entities.organism import Organism, create_organism

    assert Organism is not None
    assert create_organism is not None
