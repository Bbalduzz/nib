# System Monitor

A dashboard application that displays battery, network, display, and thermal information using Nib's system services. Demonstrates `on_appear` for automatic data refresh, card-style layouts, and conditional styling.

## Full Source

```python
import nib
from nib.services.battery import ThermalState

def main(app: nib.App):
    app.title = "System Info"
    app.icon = nib.SFSymbol("info.circle.fill")
    app.width = 360
    app.height = 520

    # Theme colors
    card_bg = "#1C1C1E"
    text_secondary = "#8E8E93"
    green = "#30D158"
    blue = "#0A84FF"
    orange = "#FF9F0A"
    red = "#FF453A"

    # ── Helpers ──────────────────────────────────────────────

    def make_card(title, *controls):
        return nib.VStack(
            controls=[
                nib.Text(title, font=nib.Font.CAPTION, foreground_color=text_secondary),
                *controls,
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=8,
            padding=12,
            background=nib.Rectangle(corner_radius=10, fill=card_bg, opacity=0.6),
        )

    def make_row(icon, label, value_view, icon_color=None):
        return nib.HStack(
            controls=[
                nib.SFSymbol(icon, font=nib.Font.system(14),
                             foreground_color=icon_color or text_secondary),
                nib.Text(label, foreground_color=text_secondary),
                nib.Spacer(),
                value_view,
            ],
            spacing=8,
        )

    # ── Battery ──────────────────────────────────────────────

    battery_level = nib.Text("--", font=nib.Font.system(24, weight=nib.FontWeight.BOLD))
    battery_state = nib.Text("--", font=nib.Font.CAPTION, foreground_color=text_secondary)
    battery_time = nib.Text("", font=nib.Font.CAPTION, foreground_color=text_secondary)

    def refresh_battery():
        try:
            info = app.battery.get_status()
            if info.has_battery and info.level is not None:
                battery_level.content = f"{info.level:.0f}%"
                if info.level >= 50:
                    battery_level.foreground_color = green
                elif info.level >= 20:
                    battery_level.foreground_color = orange
                else:
                    battery_level.foreground_color = red

                battery_state.content = info.state.value.replace("_", " ").title()

                if info.is_charging and info.time_to_full_formatted:
                    battery_time.content = f"Full in {info.time_to_full_formatted}"
                elif info.time_remaining_formatted:
                    battery_time.content = f"{info.time_remaining_formatted} remaining"
                else:
                    battery_time.content = ""
            else:
                battery_level.content = "AC"
                battery_level.foreground_color = blue
                battery_state.content = "No Battery"
        except Exception:
            battery_level.content = "N/A"

    battery_card = make_card(
        "BATTERY",
        nib.HStack(
            controls=[
                nib.VStack(
                    controls=[battery_level, battery_state],
                    alignment=nib.HorizontalAlignment.LEADING, spacing=2,
                ),
                nib.Spacer(),
                battery_time,
            ],
        ),
    )

    # ── Battery Health ───────────────────────────────────────

    health_pct = nib.Text("--", font=nib.Font.system(18, weight=nib.FontWeight.SEMIBOLD))
    health_cycles = nib.Text("--", foreground_color=text_secondary)
    health_temp = nib.Text("--", foreground_color=text_secondary)
    health_cond = nib.Text("--", foreground_color=text_secondary)

    def refresh_health():
        try:
            h = app.battery.get_health()
            if h.health_percent is not None:
                health_pct.content = f"{h.health_percent:.0f}%"
                health_pct.foreground_color = green if h.health_percent >= 80 else orange
            health_cycles.content = f"{h.cycle_count} cycles" if h.cycle_count else "N/A"
            health_temp.content = f"{h.temperature_celsius:.1f} C" if h.temperature_celsius else "N/A"
            health_cond.content = h.condition or "N/A"
        except Exception:
            health_pct.content = "N/A"

    health_card = make_card(
        "BATTERY HEALTH",
        make_row("heart.fill", "Health", health_pct, green),
        make_row("arrow.triangle.2.circlepath", "Cycles", health_cycles),
        make_row("thermometer", "Temp", health_temp),
        make_row("checkmark.shield", "Condition", health_cond),
    )

    # ── Thermal ──────────────────────────────────────────────

    thermal_text = nib.Text("--", font=nib.Font.system(16, weight=nib.FontWeight.SEMIBOLD))

    def refresh_thermal():
        try:
            t = app.battery.get_thermal_state()
            thermal_text.content = t.state.value.title()
            if t.state == ThermalState.NOMINAL:
                thermal_text.foreground_color = green
            elif t.state == ThermalState.FAIR:
                thermal_text.foreground_color = orange
            else:
                thermal_text.foreground_color = red
        except Exception:
            thermal_text.content = "N/A"

    thermal_card = make_card("THERMAL", thermal_text)

    # ── Display ──────────────────────────────────────────────

    display_name = nib.Text("--", font=nib.Font.system(14, weight=nib.FontWeight.SEMIBOLD))
    display_res = nib.Text("--", foreground_color=text_secondary)
    display_bright = nib.Text("--", foreground_color=text_secondary)
    display_refresh = nib.Text("--", foreground_color=text_secondary)

    def refresh_display():
        try:
            info = app.screen.get_info()
            display_name.content = info.name or "Display"
            display_res.content = f"{info.width:.0f} x {info.height:.0f} @{info.scale:.0f}x"
            display_bright.content = (
                f"{info.brightness * 100:.0f}%" if info.brightness is not None else "N/A"
            )
            display_refresh.content = (
                f"{info.refresh_rate:.0f} Hz" if info.refresh_rate else "N/A"
            )
        except Exception:
            display_name.content = "N/A"

    display_card = make_card(
        "DISPLAY",
        display_name,
        make_row("rectangle.on.rectangle", "Resolution", display_res),
        make_row("sun.max", "Brightness", display_bright, orange),
        make_row("speedometer", "Refresh", display_refresh),
    )

    # ── Network ──────────────────────────────────────────────

    net_status = nib.Text("--", font=nib.Font.system(16, weight=nib.FontWeight.SEMIBOLD))
    net_type = nib.Text("--", foreground_color=text_secondary)
    net_ssid = nib.Text("", foreground_color=text_secondary)

    def refresh_network():
        try:
            info = app.connectivity.get_status()
            if info.is_connected:
                net_status.content = "Connected"
                net_status.foreground_color = green
                net_type.content = info.type.value.title()
                net_ssid.content = info.ssid or ""
            else:
                net_status.content = "Offline"
                net_status.foreground_color = red
                net_type.content = "No Connection"
                net_ssid.content = ""
        except Exception:
            net_status.content = "N/A"

    network_card = make_card(
        "NETWORK",
        nib.HStack(controls=[net_status, nib.Spacer(), net_type], spacing=8),
        net_ssid,
    )

    # ── Refresh All ──────────────────────────────────────────

    def refresh_all():
        refresh_battery()
        refresh_health()
        refresh_thermal()
        refresh_display()
        refresh_network()

    app.on_appear = refresh_all

    # ── Build ────────────────────────────────────────────────

    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        battery_card,
                        health_card,
                        thermal_card,
                        display_card,
                        network_card,
                        nib.Button(
                            "Refresh All",
                            action=refresh_all,
                            style=nib.ButtonStyle.BORDERED,
                        ),
                    ],
                    spacing=10,
                    padding=12,
                ),
            ],
        )
    )

nib.run(main)
```

## Walkthrough

### Using system services

Each card fetches data from a different system service:

| Card | Service | Method |
|------|---------|--------|
| Battery | `app.battery` | `get_status()` |
| Battery Health | `app.battery` | `get_health()` |
| Thermal | `app.battery` | `get_thermal_state()` |
| Display | `app.screen` | `get_info()` |
| Network | `app.connectivity` | `get_status()` |

Services are synchronous -- call the method and use the result immediately:

```python
info = app.battery.get_status()
battery_level.content = f"{info.level:.0f}%"
```

### Refreshing on popover open

```python
app.on_appear = refresh_all
```

The `on_appear` callback fires every time the popover opens. This ensures data is fresh each time the user clicks the menu bar icon, without polling in the background.

### Card layout pattern

The `make_card` helper creates a consistent card style:

```python
def make_card(title, *controls):
    return nib.VStack(
        controls=[
            nib.Text(title, font=nib.Font.CAPTION, foreground_color=text_secondary),
            *controls,
        ],
        alignment=nib.HorizontalAlignment.LEADING,
        spacing=8,
        padding=12,
        background=nib.Rectangle(corner_radius=10, fill=card_bg, opacity=0.6),
    )
```

The `background` modifier accepts a shape view (`Rectangle`, `Circle`, etc.) to draw behind the content. Using `corner_radius` and a dark fill creates the card appearance.

### Conditional styling

The battery level color changes based on the value:

```python
if info.level >= 50:
    battery_level.foreground_color = green
elif info.level >= 20:
    battery_level.foreground_color = orange
else:
    battery_level.foreground_color = red
```

Assigning `foreground_color` triggers a UI patch, so the color updates immediately without rebuilding the entire view tree.

### Error handling

Each refresh function wraps the service call in a `try/except` block:

```python
try:
    info = app.battery.get_status()
    # ... update views
except Exception:
    battery_level.content = "N/A"
```

This prevents a service timeout or unavailable hardware (e.g., no battery on a desktop Mac) from crashing the app.

### Running

```bash
nib run system_monitor.py
```
