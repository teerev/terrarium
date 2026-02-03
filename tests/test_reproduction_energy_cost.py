from __future__ import annotations

from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.organism import Organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_cost_override_gates_and_transfers_energy() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    parent = Organism(position=Position(2, 2), energy=100, rng=world.rng)
    world.add_entity(parent)

    # With override set, rule uses cost-based mode:
    # requires energy > threshold + cost
    rule = ReproductionRule(
        reproduction_cost_override=30,
        offspring_energy_ratio=0.5,
        min_parent_energy_after=1,
    )

    offspring = rule.apply(world, world.rng)
    assert len(offspring) == 1

    child = offspring[0]
    assert child.parent_id == parent.id

    assert parent.energy == 70  # 100 - 30
    assert child.energy == 15  # int(30 * 0.5)


def test_reproduction_cost_override_requires_energy_greater_than_threshold_plus_cost() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    # Default phenotype reproduction_threshold is 10 + genome.reproduction_threshold*2;
    # with default genome reproduction_threshold=10 => phenotype threshold=30.
    parent = Organism(position=Position(1, 1), energy=50, rng=world.rng)
    world.add_entity(parent)

    # Need energy > 30 + 20 = 50; energy==50 should NOT reproduce.
    rule = ReproductionRule(reproduction_cost_override=20, offspring_energy_ratio=1.0)

    offspring = rule.apply(world, world.rng)
    assert offspring == []
    assert parent.energy == 50


def test_reproduction_cost_override_respects_min_parent_energy_after() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    parent = Organism(position=Position(0, 0), energy=100, rng=world.rng)
    world.add_entity(parent)

    # Would pass threshold+cost check (100 > 30+99), but would leave parent at 1.
    # With min_parent_energy_after=2, reproduction must not happen.
    rule = ReproductionRule(
        reproduction_cost_override=99,
        offspring_energy_ratio=1.0,
        min_parent_energy_after=2,
    )

    offspring = rule.apply(world, world.rng)
    assert offspring == []
    assert parent.energy == 100
