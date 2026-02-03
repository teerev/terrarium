from __future__ import annotations

from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.organism import Organism
from terrarium.testing import snapshot_world_state
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_creates_offspring_inherits_genome_and_lineage_and_splits_energy() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    genome = Genome(reproduction_threshold=0)
    parent = Organism(
        position=Position(2, 2),
        energy=11,
        rng=world.rng,
        genome=genome,
        birth_tick=world.tick,
    )
    world.add_entity(parent)

    rule = ReproductionRule()  # default: split-energy behavior

    offspring = rule.apply(world, world.rng)
    assert len(offspring) == 1

    child = offspring[0]
    assert child.position == parent.position
    assert child.genome == parent.genome
    assert child.parent_id == parent.id
    assert child.lineage_id == parent.lineage_id
    assert child.generation == parent.generation + 1
    assert child.birth_tick == world.tick

    # Split energy deterministically.
    assert child.energy == 11 // 2
    assert parent.energy == 11 - child.energy


def test_reproduction_is_deterministic_by_parent_id_order_and_all_can_reproduce_same_tick() -> None:
    # Use explicit ids so ordering is deterministic independent of RNG.
    w1 = WorldState(Grid(5, 5), seed=1)
    w2 = WorldState(Grid(5, 5), seed=1)

    g = Genome(reproduction_threshold=0)

    # Add in reverse order to ensure rule sorts by id.
    p2a = Organism(position=Position(0, 0), energy=10, id="b", genome=g, rng=w1.rng)
    p1a = Organism(position=Position(1, 1), energy=10, id="a", genome=g, rng=w1.rng)
    w1.add_entity(p2a)
    w1.add_entity(p1a)

    p2b = Organism(position=Position(0, 0), energy=10, id="b", genome=g, rng=w2.rng)
    p1b = Organism(position=Position(1, 1), energy=10, id="a", genome=g, rng=w2.rng)
    w2.add_entity(p2b)
    w2.add_entity(p1b)

    rule = ReproductionRule()  # default split-energy

    rule.apply(w1, w1.rng)
    rule.apply(w2, w2.rng)

    assert snapshot_world_state(w1) == snapshot_world_state(w2)


def test_reproduction_cost_is_configurable_and_offspring_energy_derived_from_cost() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    # Ensure threshold is easy to satisfy.
    genome = Genome(reproduction_threshold=0)
    parent = Organism(
        position=Position(2, 2),
        energy=20,
        rng=world.rng,
        genome=genome,
        birth_tick=world.tick,
    )
    world.add_entity(parent)

    rule = ReproductionRule(
        reproduction_cost_override=7,
        offspring_energy_ratio=0.5,
        min_parent_energy_after=1,
    )

    offspring = rule.apply(world, world.rng)
    assert len(offspring) == 1

    child = offspring[0]
    assert parent.energy == 20 - 7
    assert child.energy == int(7 * 0.5)

    # Conservation (approx due to flooring)
    assert (20 - parent.energy) >= child.energy
