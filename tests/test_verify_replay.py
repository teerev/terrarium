from __future__ import annotations

from terrarium.testing import ReplayResult, verify_replay
from terrarium.world.grid import Grid
from terrarium.world.state import WorldState
from terrarium.io.snapshot import create_snapshot


def test_verify_replay_ok_true_for_same_snapshot() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    snapshot = create_snapshot(world, world.rng)

    result = verify_replay(snapshot, n_steps=3)

    assert isinstance(result, ReplayResult)
    assert result.ok is True


def test_verify_replay_rejects_negative_steps() -> None:
    world = WorldState(Grid(5, 5), seed=123)
    snapshot = create_snapshot(world, world.rng)

    try:
        verify_replay(snapshot, n_steps=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
