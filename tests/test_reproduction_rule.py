from __future__ import annotations

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.reproduction import ReproductionRule
from terrarium.entities.genome import Genome
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_reproduction_requires_threshold_plus_cost_and_accounts_energy() -> None:
    world = WorldState(grid=Grid(5, 5), seed=123)
    rng = SeededRNG(1)

    # Choose a genome giving a stable threshold and cost via Phenotype.
    genome = Genome(reproduction_threshold=1)
    phenotype = create_organism(position=Position(0, 0), energy=0, genome=genome).phenotype
    threshold = int(phenotype.reproduction_threshold)
    cost = int(phenotype.reproduction_cost)

    parent = create_organism(
        position=Position(0, 0),
        energy=threshold + cost,  # Not strictly greater => should NOT reproduce
        rng=rng,
        genome=genome,
    )
    world.add_entity(parent)

    rule = ReproductionRule()
    spawned = rule.apply(world, rng)
    assert spawned == []

    # Now give enough energy: strictly greater than threshold + cost
    parent.energy = threshold + cost + 1

    before = parent.energy
    spawned = rule.apply(world, rng)
    assert len(spawned) == 1

    child = spawned[0]
    assert child.position == parent.position

    # Parent pays exact cost
    assert parent.energy == before - cost

    # Offspring gets energy derived from cost (default ratio 1.0, capped to cost)
    assert child.energy == cost

    # Parent retains minimum viable energy (>= 1 by default)
    assert parent.energy >= 1
