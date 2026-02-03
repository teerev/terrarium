from __future__ import annotations

from dataclasses import dataclass

from terrarium.engine.rng import SeededRNG
from terrarium.engine.rules.movement import MovementRule
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class _Phenotype:
    speed: float


@dataclass(slots=True)
class _Org:
    id: str
    position: Position
    phenotype: _Phenotype
    energy: int = 100


def test_speed_zero_is_stationary_and_costs_no_energy() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    org = _Org(id="o", position=Position(2, 2), phenotype=_Phenotype(speed=0.0), energy=10)
    world.add_entity(org)

    rule = MovementRule(allow_stay=True, base_movement_cost=5)
    rng = SeededRNG(123)

    for _ in range(50):
        rule.apply([org], world, rng)

    assert org.position == Position(2, 2)
    assert org.energy == 10


def test_speed_one_always_attempts_and_costs_base_energy_each_tick() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    org = _Org(id="o", position=Position(2, 2), phenotype=_Phenotype(speed=1.0), energy=20)
    world.add_entity(org)

    rule = MovementRule(allow_stay=True, base_movement_cost=3)
    rng = SeededRNG(999)

    # Movement attempt occurs each tick; with allow_stay=True, the position may not change,
    # but energy cost is applied for each attempted move.
    for _ in range(4):
        rule.apply([org], world, rng)

    assert org.energy == 20 - 4 * 3


def test_high_speed_moves_more_often_than_low_speed_with_same_seed() -> None:
    # Use allow_stay=False so an attempted move always results in a position change.
    rule = MovementRule(allow_stay=False)

    world_fast = WorldState(Grid(7, 7), seed=1)
    world_slow = WorldState(Grid(7, 7), seed=1)

    fast = _Org(id="f", position=Position(3, 3), phenotype=_Phenotype(speed=0.8))
    slow = _Org(id="s", position=Position(3, 3), phenotype=_Phenotype(speed=0.2))

    world_fast.add_entity(fast)
    world_slow.add_entity(slow)

    rng_fast = SeededRNG(2024)
    rng_slow = SeededRNG(2024)

    fast_moves = 0
    slow_moves = 0

    for _ in range(100):
        prev = fast.position
        rule.apply([fast], world_fast, rng_fast)
        if fast.position != prev:
            fast_moves += 1

        prev = slow.position
        rule.apply([slow], world_slow, rng_slow)
        if slow.position != prev:
            slow_moves += 1

    assert fast_moves > slow_moves
