# Battery

The Battery service provides access to battery level, charging state, health information, thermal state, and sleep prevention. Access it via `app.battery`.

```python
status = app.battery.get_status()
print(f"Level: {status.level}%")
print(f"Charging: {status.is_charging}")
```

## Methods

### `get_status()`

Get current battery status including level, charging state, and time estimates.

```python
app.battery.get_status() -> BatteryInfo
```

Returns a `BatteryInfo` dataclass.

### `get_health()`

Get battery health information including cycle count, capacity, temperature, and condition.

```python
app.battery.get_health() -> BatteryHealth
```

Returns a `BatteryHealth` dataclass.

### `get_thermal_state()`

Get the current system thermal state.

```python
app.battery.get_thermal_state() -> ThermalInfo
```

Returns a `ThermalInfo` dataclass.

### `prevent_sleep(reason, sleep_type)`

Prevent the system from sleeping. Returns an assertion that must be released later with `allow_sleep()`.

```python
app.battery.prevent_sleep(
    reason: str = "App preventing sleep",
    sleep_type: SleepType = SleepType.IDLE,
) -> SleepAssertion
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `reason` | `str` | `"App preventing sleep"` | Human-readable reason for preventing sleep |
| `sleep_type` | `SleepType` | `SleepType.IDLE` | Type of sleep to prevent |

### `allow_sleep(assertion)`

Release a sleep prevention assertion, allowing the system to sleep again.

```python
app.battery.allow_sleep(assertion: SleepAssertion | None = None) -> bool
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `assertion` | `SleepAssertion \| None` | `None` | The assertion to release. If `None`, releases the most recent assertion |

Returns `True` if the assertion was released successfully.

---

## Data Classes

### `BatteryInfo`

Battery status information returned by `get_status()`.

| Property | Type | Description |
|----------|------|-------------|
| `level` | `float \| None` | Battery level as percentage (0--100). `None` if not available |
| `is_charging` | `bool` | Whether the battery is currently charging |
| `state` | `BatteryState` | Detailed battery state enum |
| `is_low_power_mode` | `bool` | Whether Low Power Mode is enabled |
| `has_battery` | `bool` | Whether the device has a battery |
| `time_remaining` | `int \| None` | Estimated minutes until empty |
| `time_remaining_formatted` | `str \| None` | Human-readable time remaining (e.g., `"2:30"`) |
| `time_to_full` | `int \| None` | Estimated minutes until fully charged |
| `time_to_full_formatted` | `str \| None` | Human-readable time to full charge |
| `is_plugged_in` | `bool \| None` | Whether connected to power |
| `is_charged` | `bool \| None` | Whether the battery is fully charged |
| `power_source` | `str \| None` | Name of the active power source |
| `thermal_state` | `str \| None` | Current thermal state string |
| `current_capacity` | `int \| None` | Current capacity in mAh |
| `max_capacity` | `int \| None` | Maximum capacity in mAh |
| `amperage` | `int \| None` | Current amperage in mA |
| `voltage` | `float \| None` | Current voltage in V |
| `wattage` | `float \| None` | Current power draw in watts |

### `BatteryHealth`

Battery health information returned by `get_health()`.

| Property | Type | Description |
|----------|------|-------------|
| `cycle_count` | `int \| None` | Number of charge cycles completed |
| `health_percent` | `float \| None` | Battery health as a percentage of design capacity |
| `condition` | `str \| None` | Battery condition string (`"Normal"`, `"Fair"`, `"Poor"`, `"Service Recommended"`) |
| `design_capacity` | `int \| None` | Original design capacity in mAh |
| `max_capacity` | `int \| None` | Current maximum capacity in mAh |
| `temperature_celsius` | `float \| None` | Battery temperature in Celsius |
| `temperature_fahrenheit` | `float \| None` | Battery temperature in Fahrenheit |
| `manufacture_date` | `str \| None` | Battery manufacture date (YYYY-MM-DD) |
| `manufacturer` | `str \| None` | Battery manufacturer name |
| `device_name` | `str \| None` | Battery device name |
| `optimized_charging` | `bool \| None` | Whether optimized charging is engaged |

### `ThermalInfo`

Thermal state information returned by `get_thermal_state()`.

| Property | Type | Description |
|----------|------|-------------|
| `state` | `ThermalState` | Current thermal state enum value |
| `state_raw` | `int \| None` | Raw thermal state integer value |
| `recommendation` | `str \| None` | Recommendation based on thermal state |

### `SleepAssertion`

Sleep prevention assertion returned by `prevent_sleep()`.

| Property | Type | Description |
|----------|------|-------------|
| `assertion_id` | `int \| None` | System assertion ID, used to release the assertion |
| `success` | `bool` | Whether the assertion was created successfully |

---

## Enums

### `BatteryState`

```python
from nib.services.battery import BatteryState
```

| Value | Description |
|-------|-------------|
| `BatteryState.UNKNOWN` | Battery state cannot be determined |
| `BatteryState.CHARGING` | Battery is charging |
| `BatteryState.DISCHARGING` | Battery is discharging (on battery power) |
| `BatteryState.FULL` | Battery is fully charged |
| `BatteryState.NOT_CHARGING` | Battery is not charging |
| `BatteryState.PLUGGED_NOT_CHARGING` | Plugged in but not charging |
| `BatteryState.AC_POWER` | Running on AC power |

### `ThermalState`

```python
from nib.services.battery import ThermalState
```

| Value | Description |
|-------|-------------|
| `ThermalState.NOMINAL` | Normal operating temperature |
| `ThermalState.FAIR` | Slightly elevated temperature |
| `ThermalState.SERIOUS` | High temperature; system may throttle |
| `ThermalState.CRITICAL` | Very high temperature; immediate action recommended |
| `ThermalState.UNKNOWN` | Thermal state cannot be determined |

### `SleepType`

```python
from nib.services.battery import SleepType
```

| Value | Description |
|-------|-------------|
| `SleepType.IDLE` | Prevent idle sleep (default) |
| `SleepType.DISPLAY` | Prevent display sleep |
| `SleepType.SYSTEM` | Prevent all system sleep |

---

## Examples

### Display battery status

```python
import nib

def main(app: nib.App):
    app.title = "Battery"
    app.icon = nib.SFSymbol("battery.100")
    app.width = 300
    app.height = 200

    level_text = nib.Text("--", font=nib.Font.TITLE)
    state_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)

    def refresh():
        status = app.battery.get_status()
        if status.has_battery and status.level is not None:
            level_text.content = f"{status.level:.0f}%"
            state_text.content = status.state.value.title()
        else:
            level_text.content = "AC"
            state_text.content = "No Battery"

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[level_text, state_text],
            spacing=8,
            padding=20,
        )
    )

nib.run(main)
```

### Check battery health

```python
import nib

def main(app: nib.App):
    app.title = "Health"
    app.icon = nib.SFSymbol("heart.fill")
    app.width = 300
    app.height = 250

    health_text = nib.Text("--", font=nib.Font.TITLE)
    cycles_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    temp_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    condition_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)

    def refresh():
        health = app.battery.get_health()
        if health.health_percent is not None:
            health_text.content = f"{health.health_percent:.0f}% health"
        cycles_text.content = f"{health.cycle_count} cycles" if health.cycle_count else "N/A"
        temp_text.content = (
            f"{health.temperature_celsius:.1f} C"
            if health.temperature_celsius
            else "N/A"
        )
        condition_text.content = health.condition or "N/A"

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[health_text, cycles_text, temp_text, condition_text],
            spacing=8,
            padding=20,
        )
    )

nib.run(main)
```

### Prevent sleep during a long operation

```python
import nib

def main(app: nib.App):
    app.title = "Sleep Guard"
    app.icon = nib.SFSymbol("moon.zzz")
    app.width = 300
    app.height = 150

    status = nib.Text("Sleep allowed", foreground_color=nib.Color.SECONDARY)
    assertion = None

    def toggle_sleep():
        nonlocal assertion
        if assertion is None:
            assertion = app.battery.prevent_sleep(
                reason="Running long task",
                sleep_type=nib.services.battery.SleepType.IDLE,
            )
            status.content = "Sleep prevented"
        else:
            app.battery.allow_sleep(assertion)
            assertion = None
            status.content = "Sleep allowed"

    app.build(
        nib.VStack(
            controls=[
                status,
                nib.Button("Toggle Sleep Prevention", action=toggle_sleep),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Monitor thermal state

```python
import nib
from nib.services.battery import ThermalState

def main(app: nib.App):
    app.title = "Thermal"
    app.icon = nib.SFSymbol("thermometer")
    app.width = 280
    app.height = 120

    thermal_text = nib.Text("--", font=nib.Font.TITLE)

    def refresh():
        thermal = app.battery.get_thermal_state()
        thermal_text.content = thermal.state.value.title()
        if thermal.state == ThermalState.NOMINAL:
            thermal_text.foreground_color = nib.Color.GREEN
        elif thermal.state == ThermalState.FAIR:
            thermal_text.foreground_color = nib.Color.ORANGE
        elif thermal.state in (ThermalState.SERIOUS, ThermalState.CRITICAL):
            thermal_text.foreground_color = nib.Color.RED

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[thermal_text],
            padding=20,
        )
    )

nib.run(main)
```
