from __future__ import annotations

from terrarium.engine.rules.energy import EnergyRule
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_energy_rule_applies_metabolism_and_floors_at_zero() -> None:
    world = WorldState(grid=Grid(3, 3), seed=1)

    org1 = create_organism(Position(0, 0), energy=5)
    org2 = create_organism(Position(1, 1), energy=1)
    world.add_entity(org1)
    world.add_entity(org2)

    rule = EnergyRule(metabolism_rate=2)
    rule.apply([org1, org2], world)

    assert org1.energy == 3
    assert org2.energy == 0
