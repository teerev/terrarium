from __future__ import annotations


def test_events_schema_imports() -> None:
    from terrarium.events.schema import (  # noqa: F401
        BirthEvent,
        ConsumptionEvent,
        DeathEvent,
        Event,
        MovementEvent,
    )

    assert Event is not None
    assert BirthEvent is not None
    assert DeathEvent is not None
    assert ConsumptionEvent is not None
    assert MovementEvent is not None
