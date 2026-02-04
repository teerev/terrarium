from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, TypeVar

from terrarium.events.schema import Event


EventCallback = Callable[[Event], None]


class EventEmitter:
    """Synchronous publish/subscribe event emitter.

    Design constraints:
    - Synchronous emission during simulation/rule execution
    - Deterministic behavior (no randomness; listeners invoked in subscription order)
    - Optional injection into the simulation

    Notes:
    - Supports optional event_type filtering per subscriber.
    """

    def __init__(self):
        self._listeners: List[tuple[Optional[str], EventCallback]] = []

    def subscribe(self, callback: EventCallback, event_type: str | None = None) -> None:
        """Register a listener.

        If event_type is provided, the callback only receives events matching
        event.event_type.
        """

        if not callable(callback):
            raise TypeError("callback must be callable")
        if event_type is not None and not isinstance(event_type, str):
            raise TypeError("event_type must be a str or None")
        self._listeners.append((event_type, callback))

    def emit(self, event: Event) -> None:
        """Emit an event to all subscribed listeners.

        Listeners are invoked synchronously in the order they were subscribed.
        """

        et = getattr(event, "event_type", None)
        for want_type, cb in list(self._listeners):
            if want_type is None or want_type == et:
                cb(event)


@dataclass(slots=True)
class EventLog:
    """A simple listener that collects all emitted events in order."""

    events: List[Event] = field(default_factory=list)

    def __call__(self, event: Event) -> None:
        self.events.append(event)
