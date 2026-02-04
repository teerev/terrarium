from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

try:
    import typer  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    # Minimal fallback so importing terrarium.cli works in environments without typer.
    class _DummyApp:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self._commands: list[Any] = []

        def command(self, *args: Any, **kwargs: Any):
            def deco(fn):
                self._commands.append(fn)
                return fn

            return deco

        def callback(self, *args: Any, **kwargs: Any):
            def deco(fn):
                return fn

            return deco

    class _TyperModule:
        Typer = _DummyApp

        def Argument(self, default: Any = ..., *args: Any, **kwargs: Any) -> Any:
            return default

        def Option(self, default: Any = ..., *args: Any, **kwargs: Any) -> Any:
            return default

        def echo(self, message: Any) -> None:
            print(message)

    typer = _TyperModule()  # type: ignore

from terrarium.engine.simulator import Simulator
from terrarium.io.snapshot import load_snapshot, save_snapshot
from terrarium.profiling import SimulationProfiler
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState


app = typer.Typer(add_completion=False)


@app.command()
def run(
    steps: int = typer.Argument(100, help="Number of steps to run"),
    seed: int = typer.Option(0, "--seed", help="Seed for deterministic RNG"),
    width: int = typer.Option(20, "--width", help="World width"),
    height: int = typer.Option(10, "--height", help="World height"),
    snapshot_in: Optional[Path] = typer.Option(None, "--snapshot-in", help="Load initial world snapshot"),
    snapshot_out: Optional[Path] = typer.Option(None, "--snapshot-out", help="Save final world snapshot"),
    profile: bool = typer.Option(False, "--profile", help="Print profiling timing summary"),
) -> None:
    """Run a terrarium simulation."""

    if snapshot_in is not None:
        world, rng = load_snapshot(snapshot_in)
    else:
        world = WorldState(Grid(width=width, height=height), seed=seed)
        rng = world.rng

    profiler = SimulationProfiler(enabled=True) if bool(profile) else None

    sim = Simulator(world, rng, profiler=profiler)
    sim.run(int(steps))

    if snapshot_out is not None:
        save_snapshot(snapshot_out, world, rng)

    if profiler is not None:
        typer.echo(profiler.report())
