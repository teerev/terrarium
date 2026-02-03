from __future__ import annotations

from terrarium.metrics.collector import MetricsCollector
from terrarium.world.grid import Grid, Position
from terrarium.world.state import WorldState
from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource


def test_metrics_collector_records_basic_metrics() -> None:
    world = WorldState(Grid(5, 5), seed=123)

    world.add_entity(Organism(Position(0, 0), energy=10))
    world.add_entity(Organism(Position(1, 0), energy=20))
    world.add_entity(Resource(Position(2, 0), energy_value=5))

    c = MetricsCollector(max_ticks=10)
    c.record_tick(world)

    assert c.get_current("population_count") == 2.0
    assert c.get_current("resource_count") == 1.0
    assert c.get_current("total_energy") == 30.0
    assert c.get_current("average_energy") == 15.0

    # History is time-series list[float]
    pop_hist = c.get_history("population_count")
    assert pop_hist == [2.0]


def test_metrics_collector_running_stats_and_bounded_history() -> None:
    world = WorldState(Grid(5, 5), seed=1)
    c = MetricsCollector(max_ticks=2)

    world.add_entity(Organism(Position(0, 0), energy=5))
    c.record_tick(world)

    world.step()
    world.add_entity(Organism(Position(1, 0), energy=15))
    c.record_tick(world)

    world.step()
    c.record_tick(world)

    # bounded to last 2
    assert len(c.history) == 2

    stats = c.get_stats("population_count")
    assert stats["count"] == 3.0
    assert stats["min"] == 1.0
    assert stats["max"] == 2.0
    assert stats["mean"] == (1.0 + 2.0 + 2.0) / 3.0
