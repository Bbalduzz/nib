"""Battery and power management service.

Provides access to battery level, charging state, health, thermal state,
and sleep prevention.

Example:
    Get battery status::

        status = app.battery.get_status()
        print(f"Level: {status.level}%")
        print(f"Charging: {status.is_charging}")

    Get battery health::

        health = app.battery.get_health()
        print(f"Cycle count: {health.cycle_count}")
        print(f"Health: {health.health_percent}%")

    Prevent system sleep::

        assertion = app.battery.prevent_sleep(reason="Downloading file")
        # ... do work ...
        app.battery.allow_sleep(assertion)
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
    PLUGGED_NOT_CHARGING = "pluggedNotCharging"
    AC_POWER = "acPower"


class ThermalState(Enum):
    """System thermal state."""
    NOMINAL = "nominal"
    FAIR = "fair"
    SERIOUS = "serious"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class SleepType(Enum):
    """Type of sleep prevention."""
    IDLE = "idle"  # Prevent idle sleep (default)
    DISPLAY = "display"  # Prevent display sleep
    SYSTEM = "system"  # Prevent all system sleep


@dataclass
class BatteryInfo:
    """Battery status information.

    Attributes:
        level: Battery level as percentage (0-100). None if not available.
        is_charging: Whether the battery is currently charging.
        state: Detailed battery state.
        is_low_power_mode: Whether low power mode is enabled.
        has_battery: Whether the device has a battery.
        time_remaining: Estimated minutes until empty. None if not available.
        time_to_full: Estimated minutes until fully charged. None if not available.
        is_plugged_in: Whether connected to power.
        power_source: Name of power source.
        thermal_state: Current thermal state.
        wattage: Current power draw in watts.
    """
    level: Optional[float]
    is_charging: bool
    state: BatteryState
    is_low_power_mode: bool
    has_battery: bool
    time_remaining: Optional[int] = None
    time_remaining_formatted: Optional[str] = None
    time_to_full: Optional[int] = None
    time_to_full_formatted: Optional[str] = None
    is_plugged_in: Optional[bool] = None
    is_charged: Optional[bool] = None
    power_source: Optional[str] = None
    thermal_state: Optional[str] = None
    current_capacity: Optional[int] = None
    max_capacity: Optional[int] = None
    amperage: Optional[int] = None
    voltage: Optional[float] = None
    wattage: Optional[float] = None

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
            time_remaining=data.get("timeRemaining") or data.get("timeToEmpty"),
            time_remaining_formatted=data.get("timeToEmptyFormatted"),
            time_to_full=data.get("timeToFullCharge"),
            time_to_full_formatted=data.get("timeToFullChargeFormatted"),
            is_plugged_in=data.get("isPluggedIn"),
            is_charged=data.get("isCharged"),
            power_source=data.get("powerSource"),
            thermal_state=data.get("thermalState"),
            current_capacity=data.get("currentCapacity"),
            max_capacity=data.get("maxCapacity"),
            amperage=data.get("amperage"),
            voltage=data.get("voltage"),
            wattage=data.get("wattage"),
        )


@dataclass
class BatteryHealth:
    """Battery health information.

    Attributes:
        cycle_count: Number of charge cycles.
        health_percent: Battery health as percentage of design capacity.
        condition: Battery condition string (Normal, Fair, Poor, Service Recommended).
        design_capacity: Original design capacity in mAh.
        max_capacity: Current maximum capacity in mAh.
        temperature_celsius: Battery temperature in Celsius.
        temperature_fahrenheit: Battery temperature in Fahrenheit.
        manufacture_date: Battery manufacture date (YYYY-MM-DD).
        manufacturer: Battery manufacturer.
        device_name: Battery device name.
        optimized_charging: Whether optimized charging is engaged.
    """
    cycle_count: Optional[int] = None
    health_percent: Optional[float] = None
    condition: Optional[str] = None
    design_capacity: Optional[int] = None
    max_capacity: Optional[int] = None
    temperature_celsius: Optional[float] = None
    temperature_fahrenheit: Optional[float] = None
    manufacture_date: Optional[str] = None
    manufacturer: Optional[str] = None
    device_name: Optional[str] = None
    optimized_charging: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "BatteryHealth":
        """Create BatteryHealth from dictionary response."""
        return cls(
            cycle_count=data.get("cycleCount"),
            health_percent=data.get("healthPercent"),
            condition=data.get("condition"),
            design_capacity=data.get("designCapacity"),
            max_capacity=data.get("maxCapacity"),
            temperature_celsius=data.get("temperatureCelsius"),
            temperature_fahrenheit=data.get("temperatureFahrenheit"),
            manufacture_date=data.get("manufactureDate"),
            manufacturer=data.get("manufacturer"),
            device_name=data.get("deviceName"),
            optimized_charging=data.get("optimizedChargingEngaged"),
        )


@dataclass
class ThermalInfo:
    """System thermal state information.

    Attributes:
        state: Thermal state (nominal, fair, serious, critical).
        state_raw: Raw thermal state value.
        recommendation: Recommendation based on thermal state.
    """
    state: ThermalState
    state_raw: Optional[int] = None
    recommendation: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ThermalInfo":
        """Create ThermalInfo from dictionary response."""
        state_str = data.get("thermalState", "unknown")
        try:
            state = ThermalState(state_str)
        except ValueError:
            state = ThermalState.UNKNOWN

        return cls(
            state=state,
            state_raw=data.get("thermalStateRaw"),
            recommendation=data.get("recommendation"),
        )


@dataclass
class SleepAssertion:
    """Sleep prevention assertion.

    Attributes:
        assertion_id: ID of the sleep assertion (used to release it).
        success: Whether the assertion was created successfully.
    """
    assertion_id: Optional[int] = None
    success: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "SleepAssertion":
        """Create SleepAssertion from dictionary response."""
        return cls(
            assertion_id=data.get("assertionID"),
            success=data.get("success", False),
        )


class Battery(Service):
    """Service for accessing battery and power management.

    Access via app.battery property.

    Features:
        - Get battery status (level, charging state, time estimates)
        - Get battery health (cycle count, capacity, temperature)
        - Get thermal state
        - Prevent/allow system sleep

    Example:
        Check battery level::

            status = app.battery.get_status()
            if status.level and status.level < 20:
                app.notify("Low Battery", f"{status.level}% remaining")

        Monitor battery health::

            health = app.battery.get_health()
            if health.health_percent and health.health_percent < 80:
                print("Battery may need service")
    """

    def get_status(self) -> BatteryInfo:
        """Get current battery status.

        Returns:
            BatteryInfo with current battery state, level, and time estimates.

        Example:
            Get detailed battery info::

                status = app.battery.get_status()
                print(f"Level: {status.level}%")
                print(f"State: {status.state.value}")
                if status.time_remaining:
                    print(f"Time remaining: {status.time_remaining_formatted}")
        """
        data = self._request("battery", "status")
        return BatteryInfo.from_dict(data)

    def get_health(self) -> BatteryHealth:
        """Get battery health information.

        Returns:
            BatteryHealth with cycle count, capacity, temperature, and condition.

        Example:
            Check battery health::

                health = app.battery.get_health()
                print(f"Cycle count: {health.cycle_count}")
                print(f"Health: {health.health_percent:.1f}%")
                print(f"Condition: {health.condition}")
                if health.temperature_celsius:
                    print(f"Temperature: {health.temperature_celsius:.1f}°C")
        """
        data = self._request("battery", "health")
        return BatteryHealth.from_dict(data)

    def get_thermal_state(self) -> ThermalInfo:
        """Get current thermal state.

        Returns:
            ThermalInfo with thermal state and recommendations.

        Example:
            Check thermal state::

                thermal = app.battery.get_thermal_state()
                if thermal.state == ThermalState.SERIOUS:
                    print(f"Warning: {thermal.recommendation}")
        """
        data = self._request("battery", "thermalState")
        return ThermalInfo.from_dict(data)

    def prevent_sleep(
        self,
        reason: str = "App preventing sleep",
        sleep_type: SleepType = SleepType.IDLE,
    ) -> SleepAssertion:
        """Prevent system from sleeping.

        Args:
            reason: Human-readable reason for preventing sleep.
            sleep_type: Type of sleep to prevent:
                - IDLE: Prevent idle sleep (default)
                - DISPLAY: Prevent display sleep
                - SYSTEM: Prevent all system sleep

        Returns:
            SleepAssertion with assertion ID (save this to release later).

        Example:
            Prevent sleep during download::

                assertion = app.battery.prevent_sleep(
                    reason="Downloading large file",
                    sleep_type=SleepType.IDLE,
                )
                # ... do work ...
                app.battery.allow_sleep(assertion)
        """
        data = self._request("battery", "preventSleep", {
            "reason": reason,
            "type": sleep_type.value,
        })
        return SleepAssertion.from_dict(data)

    def allow_sleep(self, assertion: Optional[SleepAssertion] = None) -> bool:
        """Allow system to sleep again.

        Args:
            assertion: The SleepAssertion to release. If None, releases
                the most recent assertion.

        Returns:
            True if sleep was allowed successfully.

        Example:
            Release sleep assertion::

                success = app.battery.allow_sleep(assertion)
        """
        params = {}
        if assertion and assertion.assertion_id:
            params["assertionID"] = assertion.assertion_id

        data = self._request("battery", "allowSleep", params if params else None)
        return data.get("success", False)
