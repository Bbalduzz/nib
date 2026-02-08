# System Services

Nib exposes native macOS services through lazy-loaded properties on the `app` object. Each service communicates with the Swift runtime via a blocking request/response pattern.

---

## Battery

Access battery level, charging state, health metrics, and thermal information.

```python
import nib

def main(app: nib.App):
    app.title = "Battery"
    app.icon = nib.SFSymbol("battery.100")
    app.width = 300
    app.height = 250

    status = app.battery.get_status()

    level_text = f"{status.level:.0f}%" if status.level else "N/A"
    state_text = status.state.value
    charging_text = "Yes" if status.is_charging else "No"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Battery Status", font=nib.Font.HEADLINE),
                nib.Divider(),
                _row("Level", level_text),
                _row("State", state_text),
                _row("Charging", charging_text),
                _row("Plugged In", "Yes" if status.is_plugged_in else "No"),
                _row("Low Power", "Yes" if status.is_low_power_mode else "No"),
            ],
            spacing=6,
            alignment=nib.HorizontalAlignment.LEADING,
            padding=16,
        )
    )

def _row(label, value):
    return nib.HStack(
        controls=[
            nib.Text(label, foreground_color=nib.Color.SECONDARY),
            nib.Spacer(),
            nib.Text(value),
        ],
    )

nib.run(main)
```

### BatteryInfo fields

| Field | Type | Description |
|-------|------|-------------|
| `level` | `float` or `None` | Battery percentage (0--100) |
| `is_charging` | `bool` | Currently charging |
| `state` | `BatteryState` | Detailed state (charging, discharging, full, etc.) |
| `is_low_power_mode` | `bool` | Low Power Mode enabled |
| `has_battery` | `bool` | Device has a battery |
| `time_remaining` | `int` or `None` | Minutes until empty |
| `time_to_full` | `int` or `None` | Minutes until fully charged |
| `is_plugged_in` | `bool` or `None` | Connected to power |
| `thermal_state` | `str` or `None` | Current thermal state |
| `wattage` | `float` or `None` | Power draw in watts |

### Battery health

```python
health = app.battery.get_health()

print(f"Cycle count: {health.cycle_count}")
print(f"Health: {health.health_percent:.1f}%")
print(f"Condition: {health.condition}")
print(f"Temperature: {health.temperature_celsius:.1f}C")
```

### Prevent sleep

```python
from nib.services.battery import SleepType

# Prevent idle sleep during a long task
assertion = app.battery.prevent_sleep(
    reason="Processing data",
    sleep_type=SleepType.IDLE,
)

# ... do work ...

# Allow sleep again
app.battery.allow_sleep(assertion)
```

---

## Connectivity

Check network status, connection type, and WiFi information.

```python
status = app.connectivity.get_status()

print(f"Connected: {status.is_connected}")
print(f"Type: {status.type.value}")       # "wifi", "ethernet", "cellular", "none"
print(f"WiFi SSID: {status.ssid}")
print(f"Expensive: {status.is_expensive}")  # True for cellular
print(f"Constrained: {status.is_constrained}")  # Low Data Mode
```

### ConnectivityInfo fields

| Field | Type | Description |
|-------|------|-------------|
| `is_connected` | `bool` | Active network connection |
| `type` | `ConnectionType` | `WIFI`, `ETHERNET`, `CELLULAR`, `NONE`, `OTHER` |
| `is_expensive` | `bool` | Metered connection (cellular) |
| `is_constrained` | `bool` | Low Data Mode active |
| `ssid` | `str` or `None` | WiFi network name |
| `interface_name` | `str` or `None` | Network interface name |

### Example: connectivity indicator

```python
status = app.connectivity.get_status()

if status.is_connected:
    icon = "wifi" if status.type.value == "wifi" else "network"
    color = nib.Color.GREEN
else:
    icon = "wifi.slash"
    color = nib.Color.RED

nib.HStack(
    controls=[
        nib.SFSymbol(icon, foreground_color=color),
        nib.Text("Online" if status.is_connected else "Offline"),
    ],
    spacing=6,
)
```

---

## Screen

Get display information, control brightness, check dark mode, and take screenshots.

### Get screen info

```python
info = app.screen.get_info()

print(f"Display: {info.name}")
print(f"Resolution: {info.width}x{info.height} @{info.scale}x")
print(f"Brightness: {info.brightness * 100:.0f}%")
print(f"Refresh rate: {info.refresh_rate}Hz")
print(f"Native: {info.native_width}x{info.native_height}")
```

### Set brightness

```python
app.screen.set_brightness(0.5)  # 50% brightness
```

!!! note
    Brightness control only works on the built-in display.

### Dark mode

```python
# Check dark mode
dark_info = app.screen.get_dark_mode()
print(f"Dark mode: {dark_info.is_dark_mode}")

# Toggle dark mode (requires Accessibility permission for System Events)
app.screen.set_dark_mode(True)
app.screen.set_dark_mode(False)
```

### List displays

```python
displays = app.screen.list_displays()
for d in displays:
    print(f"{d['name']}: {d['width']}x{d['height']} @{d['scale']}x")
```

### Take a screenshot

```python
result = app.screen.screenshot()
if result.success:
    result.save("/tmp/screenshot.png")
    print(f"Saved {result.width}x{result.height} screenshot")

# Capture a specific region
result = app.screen.screenshot(x=0, y=0, width=500, height=500)
```

!!! warning
    Screenshots require the Screen Recording permission. macOS will prompt the user on first use.

---

## Keychain

Store and retrieve sensitive data (passwords, API tokens) securely in the macOS Keychain.

```python
# Store a credential
app.keychain.set("MyApp", "user@example.com", "secret-password")

# Retrieve a credential
password = app.keychain.get("MyApp", "user@example.com")
if password:
    print(f"Password: {password}")

# Check if an entry exists
if app.keychain.exists("MyApp", "user@example.com"):
    print("Credential found")

# Delete a credential
app.keychain.delete("MyApp", "user@example.com")
```

### Method reference

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set` | `service, account, password` | `bool` | Store or update a credential |
| `get` | `service, account` | `str` or `None` | Retrieve a credential |
| `delete` | `service, account` | `bool` | Delete a credential |
| `exists` | `service, account` | `bool` | Check if a credential exists |

!!! tip
    Use the app name as the `service` parameter and a username or identifier as the `account` parameter.

---

## Camera

List camera devices, capture photos, and stream video frames.

### List devices

```python
devices = app.camera.list_devices()
for device in devices:
    print(f"{device.name} (id={device.id}, position={device.position.value})")
```

### Capture a photo

```python
# Capture with the default camera
frame = app.camera.capture_photo()
frame.save("/tmp/photo.jpg")
print(f"Captured {frame.width}x{frame.height} {frame.format}")

# Capture with a specific device
frame = app.camera.capture_photo(device_id="some-device-id", format="png")
```

### Stream video frames

```python
from nib.services.camera import CameraFrame

def on_frame(frame: CameraFrame):
    # Process frame (e.g., for ML inference)
    print(f"Frame: {frame.width}x{frame.height}")

# Start streaming at 15 FPS
app.camera.start_stream(on_frame, fps=15)

# Later, stop streaming
app.camera.stop_stream()
```

!!! warning
    Camera access requires the Camera permission. Use `app.permissions.request(nib.Permission.CAMERA)` to request it.

---

## Launch at Login

Enable or disable automatic app launch when the user logs in. Uses `SMAppService` on macOS 13+.

```python
# Check current state
if app.launch_at_login.is_enabled:
    print("App launches at login")

# Enable (always in response to user action)
app.launch_at_login.set(True)

# Disable
app.launch_at_login.set(False)
```

### Toggle with a control

```python
nib.Toggle(
    "Launch at Login",
    is_on=app.launch_at_login.is_enabled,
    on_change=lambda is_on: app.launch_at_login.set(is_on),
)
```

!!! warning
    Per Mac App Store guidelines, Launch at Login should only be enabled in direct response to a user action (e.g., a toggle or button click). Do not enable it silently.

---

## Permissions

Check and request Camera, Microphone, and Notification permissions through a unified API.

### Check a permission

```python
from nib.services.permissions import Permission, PermissionStatus

status = app.permissions.check(Permission.CAMERA)

if status == PermissionStatus.AUTHORIZED:
    print("Camera access granted")
elif status == PermissionStatus.NOT_DETERMINED:
    print("Permission not yet requested")
elif status == PermissionStatus.DENIED:
    print("Camera access denied")
elif status == PermissionStatus.RESTRICTED:
    print("Camera access restricted by policy")
```

### Request a permission

```python
granted = app.permissions.request(Permission.CAMERA)
if granted:
    print("Camera access granted")
else:
    print("Camera access denied")
```

### Available permissions

| Permission | Constant |
|-----------|----------|
| Camera | `Permission.CAMERA` |
| Microphone | `Permission.MICROPHONE` |
| Notifications | `Permission.NOTIFICATIONS` |

### Permission flow example

```python
import nib
from nib.services.permissions import Permission, PermissionStatus

def main(app: nib.App):
    app.title = "Permissions"
    app.icon = nib.SFSymbol("lock.shield")
    app.width = 280
    app.height = 200

    status_label = nib.Text("Checking...", foreground_color=nib.Color.SECONDARY)

    def check_camera():
        status = app.permissions.check(Permission.CAMERA)
        if status == PermissionStatus.AUTHORIZED:
            status_label.content = "Camera: Authorized"
        elif status == PermissionStatus.NOT_DETERMINED:
            granted = app.permissions.request(Permission.CAMERA)
            status_label.content = f"Camera: {'Authorized' if granted else 'Denied'}"
        else:
            status_label.content = f"Camera: {status.value}"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Permission Check", font=nib.Font.HEADLINE),
                nib.Button("Check Camera", action=check_camera),
                status_label,
            ],
            spacing=12,
            padding=24,
        )
    )

nib.run(main)
```
