"""Base service class with synchronous request/response handling."""

import uuid
from typing import TYPE_CHECKING, Optional

from ..core.pending import PendingRequests

if TYPE_CHECKING:
    from ..core.app import App

# Shared thread-safe storage for all service requests
_requests = PendingRequests()


class Service:
    """Base class for services that communicate with Swift runtime.

    Provides synchronous request/response handling by blocking until
    the response arrives.
    """

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
        _requests.create(request_id)

        # Send request
        self._app._connection.send_service_query(service, action, request_id, params)

        # Wait for response
        result = _requests.wait(request_id, timeout)
        if result is None:
            raise TimeoutError(f"Service request timed out: {service}.{action}")

        return result

    @classmethod
    def _handle_response(cls, request_id: str, data: dict) -> None:
        """Handle response from Swift runtime (called by connection)."""
        _requests.resolve(request_id, data)
