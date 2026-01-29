"""Battery status service.

Provides access to battery level and charging state information.

Example:
    Get battery status::

        status = app.battery.get_status()
        print(f"Level: {status.level}%")
        print(f"Charging: {status.is_charging}")
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


class BatteryState(Enum):
    """Battery charging state."""
    UNKNOWN = "unknown"
    CHARGING = "charging"
    DISCHARGING = "discharging"
    FULL = "full"
    NOT_CHARGING = "notCharging"
    AC_POWER = "acPower"


@dataclass
class BatteryInfo:
    """Battery status information.

    Attributes:
        level: Battery level as percentage (0-100). None if not available.
        is_charging: Whether the battery is currently charging.
        state: Detailed battery state.
        is_low_power_mode: Whether low power mode is enabled.
        has_battery: Whether the device has a battery.
        time_remaining: Estimated minutes remaining. None if not available.
    """
    level: Optional[float]
    is_charging: bool
    state: BatteryState
    is_low_power_mode: bool
    has_battery: bool
    time_remaining: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "BatteryInfo":
        """Create BatteryInfo from dictionary response."""
        state_str = data.get("state", "unknown")
        try:
            state = BatteryState(state_str)
        except ValueError:
            state = BatteryState.UNKNOWN

        return cls(
            level=data.get("level"),
            is_charging=data.get("isCharging", False),
            state=state,
            is_low_power_mode=data.get("isLowPowerMode", False),
            has_battery=data.get("hasBattery", True),
            time_remaining=data.get("timeRemaining"),
        )


class Battery(Service):
    """Service for accessing battery information.

    Access via app.battery property.

    Example:
        Check battery level::

            status = app.battery.get_status()
            if status.level and status.level < 20:
                app.notify("Low Battery", f"{status.level}% remaining")
    """

    def get_status(self) -> BatteryInfo:
        """Get current battery status.

        Returns:
            BatteryInfo with current battery state.

        Example:
            Get battery info::

                status = app.battery.get_status()
                print(f"Level: {status.level}%")
        """
        data = self._request("battery", "status")
        return BatteryInfo.from_dict(data)
