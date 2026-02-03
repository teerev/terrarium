from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Type

from terrarium.events.schema import Event


Listener = Callable[[Event], None]


class EventEmitter:
    """Synchronous event emitter.

    - Deterministic: does not use RNG or mutate simulation state.
    - Synchronous: listeners run immediately in emission order.
    - Supports multiple listeners per event type.

    Subscriptions
    -------------
    - subscribe(callback): receive all events.
    - subscribe(callback, event_type=...) : receive only events matching event.event_type.
    - subscribe(callback, event_cls=...) : receive only instances of a specific event class.

    If filters are combined, both must match.
    """

    def __init__(self) -> None:
        self._all: List[Listener] = []
        self._by_type: Dict[str, List[Listener]] = {}
        self._by_cls: Dict[Type[object], List[Listener]] = {}

    def subscribe(
        self,
        callback: Listener,
        *,
        event_type: str | None = None,
        event_cls: Type[object] | None = None,
    ) -> None:
        if event_type is None and event_cls is None:
            self._all.append(callback)
            return

        if event_type is not None:
            self._by_type.setdefault(str(event_type), []).append(callback)

        if event_cls is not None:
            self._by_cls.setdefault(event_cls, []).append(callback)

    def emit(self, event: Event) -> None:
        # Listeners are called in deterministic order:
        #   1) global listeners (subscription order)
        #   2) event_type listeners (subscription order)
        #   3) event_cls listeners for matching classes (subscription order)
        # This may call the same callback multiple times if subscribed through
        # multiple paths; that behavior is intentional and explicit.

        for cb in list(self._all):
            cb(event)

        et = str(getattr(event, "event_type", ""))
        for cb in list(self._by_type.get(et, [])):
            cb(event)

        for cls, callbacks in list(self._by_cls.items()):
            if isinstance(event, cls):
                for cb in list(callbacks):
                    cb(event)


@dataclass(slots=True)
class EventLog:
    """Listener that collects all observed events in order."""

    events: List[Event] = field(default_factory=list)

    def __call__(self, event: Event) -> None:
        self.events.append(event)
