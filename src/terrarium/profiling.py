from __future__ import annotations

import math
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Mapping, Optional


@dataclass(frozen=True, slots=True)
class _PhaseStats:
    count: int
    total_s: float
    mean_s: float
    min_s: float
    max_s: float
    p50_s: float
    p90_s: float
    p99_s: float


class SimulationProfiler:
    """Aggregate wall-clock timing for simulation steps and named phases.

    Design goals
    ------------
    - Minimal overhead when disabled: callers can pass profiler=None.
    - Uses time.perf_counter() for accurate timing.
    - Aggregates per phase as a list of durations for summary statistics.

    Public API
    ---------
    - enabled: bool
    - time_step() -> context manager
    - time_phase(name) -> context manager
    - report() -> str
    """

    def __init__(
        self,
        *,
        enabled: bool = True,
        percentiles: Iterable[int] = (50, 90, 99),
    ) -> None:
        self.enabled = bool(enabled)
        self._step_times: List[float] = []
        self._phases: Dict[str, List[float]] = {}
        self._percentiles = tuple(int(p) for p in percentiles)

    @contextmanager
    def time_step(self) -> Iterator[None]:
        if not self.enabled:
            yield
            return

        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self._step_times.append(end - start)

    @contextmanager
    def time_phase(self, name: str) -> Iterator[None]:
        if not self.enabled:
            yield
            return

        key = str(name)
        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self._phases.setdefault(key, []).append(end - start)

    def _percentile(self, samples: List[float], pct: int) -> float:
        if not samples:
            return 0.0
        s = sorted(samples)
        if len(s) == 1:
            return float(s[0])
        p = float(pct) / 100.0
        idx = (len(s) - 1) * p
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return float(s[lo])
        frac = idx - lo
        return float(s[lo] * (1.0 - frac) + s[hi] * frac)

    def _stats(self, samples: List[float]) -> _PhaseStats:
        if not samples:
            return _PhaseStats(
                count=0,
                total_s=0.0,
                mean_s=0.0,
                min_s=0.0,
                max_s=0.0,
                p50_s=0.0,
                p90_s=0.0,
                p99_s=0.0,
            )

        total = float(sum(samples))
        count = int(len(samples))
        mean = total / count if count else 0.0
        mn = float(min(samples))
        mx = float(max(samples))
        return _PhaseStats(
            count=count,
            total_s=total,
            mean_s=mean,
            min_s=mn,
            max_s=mx,
            p50_s=self._percentile(samples, 50),
            p90_s=self._percentile(samples, 90),
            p99_s=self._percentile(samples, 99),
        )

    def get_phase_names(self) -> List[str]:
        return sorted(self._phases.keys())

    def get_phase_samples(self) -> Mapping[str, List[float]]:
        return self._phases

    def report(self) -> str:
        """Return a human-readable profiling summary."""

        step_stats = self._stats(self._step_times)
        lines: List[str] = []
        lines.append("Terrarium profiling summary")
        lines.append("--------------------------")

        steps = step_stats.count
        lines.append(f"Steps: {steps}")
        lines.append(f"Total time: {step_stats.total_s:.6f}s")
        if steps:
            lines.append(f"Per-step avg: {step_stats.mean_s:.6f}s")
            lines.append(f"Per-step min/max: {step_stats.min_s:.6f}s / {step_stats.max_s:.6f}s")
            lines.append(
                f"Per-step p50/p90/p99: {step_stats.p50_s:.6f}s / {step_stats.p90_s:.6f}s / {step_stats.p99_s:.6f}s"
            )

        lines.append("")
        lines.append("Per-phase breakdown")
        lines.append("-------------------")

        if not self._phases:
            lines.append("(no phase timings recorded)")
            return "\n".join(lines)

        # Sort by total time descending for easier bottleneck detection.
        phase_items = [(name, self._stats(samples)) for name, samples in self._phases.items()]
        phase_items.sort(key=lambda it: it[1].total_s, reverse=True)

        header = "{:<16} {:>8} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
            "phase",
            "count",
            "total(s)",
            "mean(s)",
            "min(s)",
            "max(s)",
            "p50(s)",
            "p90(s)",
        )
        lines.append(header)
        lines.append("{:<16} {:>8} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format(
            "-" * 16,
            "-" * 8,
            "-" * 10,
            "-" * 10,
            "-" * 10,
            "-" * 10,
            "-" * 10,
            "-" * 10,
        ))

        for name, st in phase_items:
            lines.append(
                "{:<16} {:>8d} {:>10.6f} {:>10.6f} {:>10.6f} {:>10.6f} {:>10.6f} {:>10.6f}".format(
                    str(name)[:16],
                    int(st.count),
                    float(st.total_s),
                    float(st.mean_s),
                    float(st.min_s),
                    float(st.max_s),
                    float(st.p50_s),
                    float(st.p90_s),
                )
            )

        # Include p99 lines if requested; keep output compact otherwise.
        if 99 in self._percentiles:
            lines.append("")
            lines.append("p99 by phase")
            lines.append("------------")
            for name, st in phase_items:
                lines.append(f"{str(name)}: {st.p99_s:.6f}s")

        return "\n".join(lines)


# Backwards/acceptance convenience alias.
Profiler = SimulationProfiler
