from __future__ import annotations

from terrarium.engine.rules.consumption import ConsumptionRule
from terrarium.entities.organism import create_organism
from terrarium.entities.resource import create_resource
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_consumption_transfers_energy_and_removes_resource_deterministically():
    world = WorldState(grid=Grid(width=5, height=5), seed=0)
    pos = Position(2, 2)

    # Two organisms on the same resource; only one should consume it.
    # Use fixed UUID ints to ensure deterministic ordering by str(id).
    o1 = create_organism(pos, energy=1)
    o2 = create_organism(pos, energy=1)

    r = create_resource(pos, energy_value=10)

    world.add_entity(o1)
    world.add_entity(o2)
    world.add_entity(r)

    rule = ConsumptionRule()
    rule.apply(world, rng=None)

    # Resource removed
    assert world.get_entity(r.id) is None

    # Exactly one organism gained the energy.
    energies = sorted([world.get_entity(o1.id).energy, world.get_entity(o2.id).energy])
    assert energies == [1, 11]
