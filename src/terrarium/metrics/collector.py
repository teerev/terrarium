from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List

from terrarium.entities.organism import Organism
from terrarium.entities.resource import Resource
from terrarium.world.state import WorldState


@dataclass(frozen=True, slots=True)
class TickMetrics:
    """Per-tick metrics snapshot."""

    tick: int

    population_count: int
    birth_count: int
    death_count: int

    total_energy: float
    average_energy: float
    resource_count: int


class MetricsCollector:
    """Collects and stores simulation metrics over time.

    Metrics are computed at the end of each tick via :meth:`record_tick`.

    Notes
    -----
    - History is bounded by ``max_ticks``.
    - Birth/death counts are best-effort:
        * If the provided world has an ``event_log`` attribute with an ``events`` list,
          BirthEvent and DeathEvent instances are counted for the *current* tick.
        * Otherwise birth/death counts are derived from population deltas.
    """

    def __init__(self, *, max_ticks: int = 1000) -> None:
        if int(max_ticks) <= 0:
            raise ValueError("max_ticks must be positive")
        self._history: Deque[TickMetrics] = deque(maxlen=int(max_ticks))

        # Running stats per metric.
        self._stats: Dict[str, Dict[str, float]] = {}

        # State to compute deltas when events are not available.
        self._last_population: int | None = None
        self._last_tick_seen: int | None = None

    def record_tick(self, world: WorldState) -> None:
        tick = int(world.tick)

        organisms, resources = self._iter_entities(world)

        population = len(organisms)
        total_energy = float(sum(int(o.energy) for o in organisms))
        avg_energy = float(total_energy / population) if population > 0 else 0.0
        resource_count = len(resources)

        birth_count, death_count = self._counts_for_tick(world, tick, population)

        snap = TickMetrics(
            tick=tick,
            population_count=int(population),
            birth_count=int(birth_count),
            death_count=int(death_count),
            total_energy=float(total_energy),
            average_energy=float(avg_energy),
            resource_count=int(resource_count),
        )

        self._history.append(snap)
        self._update_stats(snap)

        self._last_population = int(population)
        self._last_tick_seen = int(tick)

    def get_history(self, metric_name: str) -> List[float]:
        name = str(metric_name)
        return [float(getattr(s, name)) for s in self._history]

    def get_current(self, metric_name: str) -> float:
        if not self._history:
            raise KeyError("no metrics recorded")
        name = str(metric_name)
        return float(getattr(self._history[-1], name))

    def get_stats(self, metric_name: str) -> dict[str, float]:
        """Return running statistics for a metric.

        Returns a dict with keys: count, mean, min, max.
        """

        name = str(metric_name)
        if name not in self._stats:
            raise KeyError(name)
        # return a shallow copy to prevent external mutation
        return dict(self._stats[name])

    @property
    def history(self) -> List[TickMetrics]:
        return list(self._history)

    def attach(self, simulator: object) -> None:
        """Attach to a simulator-like object via a tick callback.

        Best-effort integration:
        - If ``simulator`` has an ``on_tick`` method that accepts a callback,
          subscribe ``self.record_tick``.
        """

        on_tick = getattr(simulator, "on_tick", None)
        if callable(on_tick):
            on_tick(self.record_tick)

    def _iter_entities(self, world: WorldState) -> tuple[list[Organism], list[Resource]]:
        # WorldState stores entities in a private dict; use it for performance.
        # This mirrors existing patterns in terrarium.testing.snapshot_world_state.
        entities: Iterable[object] = list(world._entities.values())  # type: ignore[attr-defined]

        organisms: list[Organism] = []
        resources: list[Resource] = []
        for e in entities:
            if isinstance(e, Organism):
                organisms.append(e)
            elif isinstance(e, Resource):
                resources.append(e)
        return organisms, resources

    def _counts_for_tick(self, world: WorldState, tick: int, population: int) -> tuple[int, int]:
        # 1) Prefer event log if present.
        try:
            event_log = getattr(world, "event_log", None)
            events = getattr(event_log, "events", None)
            if isinstance(events, list):
                from terrarium.events.schema import BirthEvent, DeathEvent

                births = 0
                deaths = 0
                for ev in events:
                    if getattr(ev, "tick", None) != tick:
                        continue
                    if isinstance(ev, BirthEvent):
                        births += 1
                    elif isinstance(ev, DeathEvent):
                        deaths += 1
                return births, deaths
        except Exception:
            # Fall back to delta-based counts.
            pass

        # 2) Delta-based fallback (cannot distinguish births from deaths beyond net change).
        if self._last_population is None or self._last_tick_seen is None:
            return 0, 0

        if int(tick) == int(self._last_tick_seen):
            # Already recorded this tick; avoid double counting.
            return 0, 0

        delta = int(population) - int(self._last_population)
        if delta >= 0:
            return int(delta), 0
        return 0, int(-delta)

    def _update_stats(self, snap: TickMetrics) -> None:
        for name in (
            "population_count",
            "birth_count",
            "death_count",
            "total_energy",
            "average_energy",
            "resource_count",
        ):
            value = float(getattr(snap, name))
            st = self._stats.get(name)
            if st is None:
                self._stats[name] = {
                    "count": 1.0,
                    "mean": float(value),
                    "min": float(value),
                    "max": float(value),
                }
                continue

            count = float(st["count"]) + 1.0
            mean = float(st["mean"]) + (value - float(st["mean"])) / count
            st["count"] = count
            st["mean"] = float(mean)
            st["min"] = float(min(float(st["min"]), value))
            st["max"] = float(max(float(st["max"]), value))
