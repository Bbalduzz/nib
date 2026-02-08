# Connectivity

The Connectivity service provides access to network status and connection type information. Access it via `app.connectivity`.

```python
status = app.connectivity.get_status()
print(f"Connected: {status.is_connected}")
print(f"Type: {status.type}")
```

## Methods

### `get_status()`

Get the current network connectivity status.

```python
app.connectivity.get_status() -> ConnectivityInfo
```

Returns a `ConnectivityInfo` dataclass with all network details.

---

## Data Classes

### `ConnectivityInfo`

Network connectivity information returned by `get_status()`.

| Property | Type | Description |
|----------|------|-------------|
| `is_connected` | `bool` | Whether there is an active network connection |
| `type` | `ConnectionType` | The type of network connection |
| `is_expensive` | `bool` | Whether the connection is metered/expensive (e.g., cellular) |
| `is_constrained` | `bool` | Whether the connection is constrained (Low Data Mode) |
| `ssid` | `str \| None` | Wi-Fi network name if connected to Wi-Fi, `None` otherwise |
| `interface_name` | `str \| None` | Name of the active network interface (e.g., `"en0"`) |

---

## Enums

### `ConnectionType`

```python
from nib.services.connectivity import ConnectionType
```

| Value | Description |
|-------|-------------|
| `ConnectionType.NONE` | No active connection |
| `ConnectionType.WIFI` | Connected via Wi-Fi |
| `ConnectionType.ETHERNET` | Connected via Ethernet |
| `ConnectionType.CELLULAR` | Connected via cellular data |
| `ConnectionType.OTHER` | Connected via an unrecognized interface |

---

## Examples

### Display network status

```python
import nib

def main(app: nib.App):
    app.title = "Network"
    app.icon = nib.SFSymbol("wifi")
    app.width = 300
    app.height = 200

    status_text = nib.Text("--", font=nib.Font.TITLE)
    type_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    ssid_text = nib.Text("", foreground_color=nib.Color.SECONDARY)

    def refresh():
        info = app.connectivity.get_status()
        if info.is_connected:
            status_text.content = "Connected"
            status_text.foreground_color = nib.Color.GREEN
            type_text.content = info.type.value.title()
            ssid_text.content = info.ssid or ""
        else:
            status_text.content = "Offline"
            status_text.foreground_color = nib.Color.RED
            type_text.content = "No Connection"
            ssid_text.content = ""

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[
                status_text,
                type_text,
                ssid_text,
                nib.Button("Refresh", action=refresh),
            ],
            spacing=8,
            padding=20,
        )
    )

nib.run(main)
```

### Warn on expensive connections

```python
import nib

def main(app: nib.App):
    app.title = "Net Check"
    app.icon = nib.SFSymbol("antenna.radiowaves.left.and.right")
    app.width = 320
    app.height = 150

    label = nib.Text("Checking...", font=nib.Font.BODY)

    def check_connection():
        info = app.connectivity.get_status()
        if not info.is_connected:
            label.content = "No network connection available."
            app.notify("Offline", "Connect to the internet to continue.")
        elif info.is_expensive:
            label.content = f"Metered connection ({info.type.value}). Downloads paused."
        elif info.is_constrained:
            label.content = "Low Data Mode active. Limiting bandwidth."
        else:
            label.content = f"Connected via {info.type.value.title()}. All systems go."

    app.on_appear = check_connection

    app.build(
        nib.VStack(controls=[label], padding=20)
    )

nib.run(main)
```
