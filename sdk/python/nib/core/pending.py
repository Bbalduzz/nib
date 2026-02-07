"""Thread-safe pending request/response tracking.

Provides a shared class for modules that need to send a request to the
Swift runtime and block until the response arrives.  All dict access is
guarded by a single lock so concurrent socket-read and caller threads
cannot race.
"""

import threading
from typing import Any, Dict, Optional


class PendingRequests:
    """Thread-safe storage for in-flight request/response pairs.

    Usage::

        _pending = PendingRequests()

        # Caller thread
        _pending.create(request_id)
        connection.send(...)
        result = _pending.wait(request_id, timeout=5.0)

        # Socket-read thread
        _pending.resolve(request_id, value)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: Dict[str, threading.Event] = {}
        self._responses: Dict[str, Any] = {}

    def create(self, request_id: str) -> None:
        """Register a new pending request."""
        with self._lock:
            self._events[request_id] = threading.Event()

    def resolve(self, request_id: str, value: Any) -> None:
        """Store the result and wake the waiting thread."""
        with self._lock:
            event = self._events.get(request_id)
            if event is None:
                return
            self._responses[request_id] = value
            event.set()

    def wait(self, request_id: str, timeout: float = 5.0) -> Optional[Any]:
        """Block until the request is resolved or *timeout* elapses.

        Returns the resolved value, or ``None`` on timeout.
        Always cleans up internal state before returning.
        """
        with self._lock:
            event = self._events.get(request_id)
        if event is None:
            return None

        event.wait(timeout=timeout)

        with self._lock:
            self._events.pop(request_id, None)
            return self._responses.pop(request_id, None)

    def clear(self) -> None:
        """Wake all waiters and discard all state (for teardown)."""
        with self._lock:
            for event in self._events.values():
                event.set()
            self._events.clear()
            self._responses.clear()
