"""Base service class with synchronous request/response handling."""

import threading
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ..core.app import App


class Service:
    """Base class for services that communicate with Swift runtime.

    Provides synchronous request/response handling by blocking until
    the response arrives.
    """

    # Class-level storage for pending responses
    _pending: Dict[str, threading.Event] = {}
    _responses: Dict[str, dict] = {}

    def __init__(self, app: "App"):
        self._app = app

    def _request(
        self,
        service: str,
        action: str,
        params: Optional[dict] = None,
        timeout: float = 10.0,
    ) -> dict:
        """Send a synchronous request to the Swift runtime.

        Args:
            service: Service name (e.g., "battery", "camera")
            action: Action to perform (e.g., "status", "listDevices")
            params: Optional parameters for the action
            timeout: Maximum time to wait for response in seconds

        Returns:
            Response data dictionary

        Raises:
            TimeoutError: If response doesn't arrive within timeout
        """
        request_id = str(uuid.uuid4())
        event = threading.Event()

        # Register pending request
        Service._pending[request_id] = event

        # Send request
        self._app._connection.send_service_query(service, action, request_id, params)

        # Wait for response
        if not event.wait(timeout=timeout):
            Service._pending.pop(request_id, None)
            raise TimeoutError(f"Service request timed out: {service}.{action}")

        # Get and return response
        response = Service._responses.pop(request_id, {})
        Service._pending.pop(request_id, None)

        return response

    @classmethod
    def _handle_response(cls, request_id: str, data: dict) -> None:
        """Handle response from Swift runtime (called by connection)."""
        if request_id in cls._pending:
            cls._responses[request_id] = data
            cls._pending[request_id].set()
