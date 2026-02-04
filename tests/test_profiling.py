from __future__ import annotations

from terrarium.profiling import SimulationProfiler


def test_simulation_profiler_tracks_phase_and_step() -> None:
    p = SimulationProfiler(enabled=True)

    with p.time_step():
        with p.time_phase("movement"):
            pass

    report = p.report()
    assert "Terrarium profiling summary" in report
    assert "Per-phase breakdown" in report
    assert "movement" in report
