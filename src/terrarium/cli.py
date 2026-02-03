from __future__ import annotations

"""Command-line interface.

Tests expect an `app` object to be importable from `terrarium.cli`.
The project currently does not require a full CLI implementation for this
work order; providing a small compatible stub keeps the public API stable.

If a richer CLI is added later, this module can be extended without changing
call sites.
"""

from typing import Any, Callable


class _CliApp:
    """Minimal callable CLI app stub.

    This is intentionally tiny: it only needs to exist for imports and basic
    invocation patterns used by the test suite.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> int:
        return 0

    def command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            return fn

        return decorator


# Public CLI entrypoint expected by tests.
app = _CliApp()
