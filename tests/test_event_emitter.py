from __future__ import annotations

from terrarium.events.emitter import EventEmitter, EventLog
from terrarium.events.schema import MovementEvent
from terrarium.core import EntityId
from terrarium.world.grid import Position


def test_event_emitter_emits_to_all_listeners_in_order() -> None:
    emitter = EventEmitter()

    calls: list[str] = []

    def a(_evt) -> None:
        calls.append("a")

    def b(_evt) -> None:
        calls.append("b")

    emitter.subscribe(a)
    emitter.subscribe(b)

    evt = MovementEvent(
        tick=1,
        organism_id=EntityId("o1"),
        from_position=Position(0, 0),
        to_position=Position(1, 0),
    )
    emitter.emit(evt)

    assert calls == ["a", "b"]


def test_event_log_collects_events_in_emission_order() -> None:
    emitter = EventEmitter()
    log = EventLog()
    emitter.subscribe(log)

    e1 = MovementEvent(
        tick=1,
        organism_id=EntityId("o1"),
        from_position=Position(0, 0),
        to_position=Position(1, 0),
    )
    e2 = MovementEvent(
        tick=2,
        organism_id=EntityId("o1"),
        from_position=Position(1, 0),
        to_position=Position(2, 0),
    )

    emitter.emit(e1)
    emitter.emit(e2)

    assert log.events == [e1, e2]
