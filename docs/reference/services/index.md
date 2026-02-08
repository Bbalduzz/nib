# Services

Nib provides access to macOS system services through properties on the `App` instance. Each service communicates with the Swift runtime over the same socket used for view rendering, using a synchronous request/response pattern.

All services are accessed as properties on `app`:

```python
import nib

def main(app: nib.App):
    # Battery
    status = app.battery.get_status()

    # Network
    info = app.connectivity.get_status()

    # Screen
    screen = app.screen.get_info()

    # Keychain
    app.keychain.set("MyApp", "token", "secret123")

    # Camera
    devices = app.camera.list_devices()

    # Launch at Login
    app.launch_at_login.set(True)

    # Permissions
    status = app.permissions.check(nib.Permission.CAMERA)

nib.run(main)
```

## Available Services

| Service | Access | Description |
|---------|--------|-------------|
| [Battery](battery.md) | `app.battery` | Battery level, charging state, health, thermal state, and sleep prevention |
| [Connectivity](connectivity.md) | `app.connectivity` | Network connection status, type, Wi-Fi SSID, and interface info |
| [Screen](screen.md) | `app.screen` | Display resolution, brightness, dark mode, screenshots, and multi-display info |
| [Keychain](keychain.md) | `app.keychain` | Secure credential storage using the macOS Keychain |
| [Camera](camera.md) | `app.camera` | Camera device listing, photo capture, and video frame streaming |
| [LaunchAtLogin](launch-at-login.md) | `app.launch_at_login` | Control whether the app starts automatically at user login |
| [Permissions](permissions.md) | `app.permissions` | Check and request Camera, Microphone, and Notification permissions |

## How Services Work

Services extend the `Service` base class, which provides synchronous request/response communication with the Swift runtime. When you call a service method, the SDK:

1. Sends a request message over the Unix socket to the Swift runtime
2. Blocks the calling thread until a response arrives (default timeout: 10 seconds)
3. Parses the response into a typed Python dataclass and returns it

This means service calls behave like regular synchronous function calls -- no callbacks or `await` needed.

```python
# Services are synchronous -- just call and use the result
status = app.battery.get_status()
print(f"Battery: {status.level}%")
```

!!! note "Timeout"
    Service requests have a default timeout of 10 seconds. If the Swift runtime does not respond within that window, a `TimeoutError` is raised.
