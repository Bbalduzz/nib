"""Network connectivity service.

Provides access to network status and connection type information.

Example:
    Get network status::

        status = app.connectivity.get_status()
        print(f"Connected: {status.is_connected}")
        print(f"Type: {status.type}")
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


class ConnectionType(Enum):
    """Network connection type."""
    NONE = "none"
    WIFI = "wifi"
    ETHERNET = "ethernet"
    CELLULAR = "cellular"
    OTHER = "other"


@dataclass
class ConnectivityInfo:
    """Network connectivity information.

    Attributes:
        is_connected: Whether there's an active network connection.
        type: The type of network connection.
        is_expensive: Whether the connection is metered/expensive (cellular).
        is_constrained: Whether the connection is constrained (low data mode).
        ssid: WiFi network name if connected to WiFi. None otherwise.
        interface_name: Name of the active network interface.
    """
    is_connected: bool
    type: ConnectionType
    is_expensive: bool
    is_constrained: bool
    ssid: Optional[str] = None
    interface_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ConnectivityInfo":
        """Create ConnectivityInfo from dictionary response."""
        type_str = data.get("type", "none")
        try:
            conn_type = ConnectionType(type_str)
        except ValueError:
            conn_type = ConnectionType.OTHER

        return cls(
            is_connected=data.get("isConnected", False),
            type=conn_type,
            is_expensive=data.get("isExpensive", False),
            is_constrained=data.get("isConstrained", False),
            ssid=data.get("ssid"),
            interface_name=data.get("interfaceName"),
        )


class Connectivity(Service):
    """Service for accessing network connectivity information.

    Access via app.connectivity property.

    Example:
        Check network status before downloading::

            status = app.connectivity.get_status()
            if not status.is_connected:
                app.notify("Offline", "No network connection")
            elif status.is_expensive:
                app.notify("Metered Connection", "Using cellular data")
    """

    def get_status(self) -> ConnectivityInfo:
        """Get current network connectivity status.

        Returns:
            ConnectivityInfo with current network state.

        Example:
            Get network info::

                status = app.connectivity.get_status()
                print(f"Type: {status.type}")
        """
        data = self._request("connectivity", "status")
        return ConnectivityInfo.from_dict(data)
