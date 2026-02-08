# LaunchAtLogin

The LaunchAtLogin service controls whether the app starts automatically when the user logs in. It uses `SMAppService` on macOS 13+ to register the app as a login item. Access it via `app.launch_at_login`.

```python
if app.launch_at_login.is_enabled:
    print("App will launch at login")
```

!!! warning "App Store Requirement"
    Per Mac App Store guidelines, Launch at Login should only be enabled in response to a direct user action (e.g., clicking a button or toggling a switch). Do not enable it silently or at startup.

## Properties

### `is_enabled`

Read-only property that checks whether the app is currently set to launch at login.

```python
app.launch_at_login.is_enabled -> bool
```

Returns `True` if launch at login is enabled, `False` otherwise.

## Methods

### `set(enabled)`

Set the launch at login state. Call this only in response to a user action.

```python
app.launch_at_login.set(enabled: bool) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | `bool` | `True` to enable launch at login, `False` to disable |

Returns `True` if the operation was successful.

---

## Examples

### Toggle button

```python
import nib

def main(app: nib.App):
    app.title = "Settings"
    app.icon = nib.SFSymbol("gear")
    app.width = 300
    app.height = 100

    status = nib.Text("Checking...", foreground_color=nib.Color.SECONDARY)

    def toggle():
        current = app.launch_at_login.is_enabled
        app.launch_at_login.set(not current)
        status.content = "Enabled" if not current else "Disabled"

    def refresh():
        enabled = app.launch_at_login.is_enabled
        status.content = "Enabled" if enabled else "Disabled"

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[
                nib.HStack(
                    controls=[
                        nib.Text("Launch at Login"),
                        nib.Spacer(),
                        status,
                    ],
                ),
                nib.Button("Toggle", action=toggle, style=nib.ButtonStyle.BORDERED),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Toggle with on_change callback

```python
import nib

def main(app: nib.App):
    app.title = "Preferences"
    app.icon = nib.SFSymbol("gear")
    app.width = 320
    app.height = 80

    def on_change(is_on):
        app.launch_at_login.set(is_on)

    toggle = nib.Toggle(
        is_on=False,
        label="Launch at Login",
        on_change=on_change,
    )

    def refresh():
        toggle.is_on = app.launch_at_login.is_enabled

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[toggle],
            padding=20,
        )
    )

nib.run(main)
```
