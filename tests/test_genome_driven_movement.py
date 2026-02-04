from __future__ import annotations

from terrarium.engine.rules.movement import MovementRule
from terrarium.engine.rng import SeededRNG
from terrarium.entities.genome import Genome
from terrarium.entities.organism import create_organism
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


def test_genome_driven_movement_speed_probability_and_cost() -> None:
    world = WorldState(grid=Grid(5, 5), seed=123)

    # speed=0 -> phenotype speed = 0.5 (because of phenotype mapping), so set gene so phenotype clamps to 0.1?
    # For this rule we rely on phenotype output; to ensure speed=0 behavior, we must construct phenotype speed <= 0.
    # Phenotype currently clamps speed to [0.1, 3.0], so true zero probability can't be reached via genome.
    # Instead, we assert stationary behavior by using a genome that yields the minimum phenotype speed and
    # a deterministic RNG that fails the move check.
    rng = SeededRNG(1)

    slow = create_organism(
        position=Position(2, 2),
        energy=10,
        rng=rng,
        genome=Genome(speed=-999),  # phenotype clamps to 0.1
    )
    fast = create_organism(
        position=Position(1, 1),
        energy=10,
        rng=rng,
        genome=Genome(speed=0.5),  # phenotype speed = 1.0
    )

    world.add_entity(slow)
    world.add_entity(fast)

    # Use a known RNG seed so decisions are deterministic.
    rng2 = SeededRNG(42)
    rule = MovementRule(allow_stay=False, diagonals=False, base_movement_cost=2)

    # For slow organism (p=0.1), with this seed, it should often not move; for fast (p=1.0) it should always attempt.
    before_slow = slow.position
    before_fast = fast.position

    rule.apply([slow, fast], world, rng2)

    # fast should have moved (allow_stay=False; p=1.0)
    assert fast.position != before_fast
    # fast should pay energy cost proportional to speed (2 * 1.0 => 2)
    assert fast.energy == 8

    # slow may or may not move depending on rng.random(); with seed=42, first random() is ~0.639... so no move.
    assert slow.position == before_slow
    assert slow.energy == 10
