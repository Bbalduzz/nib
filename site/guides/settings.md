# Settings & Persistence

Nib provides two layers for persisting data across app launches: the high-level `Settings` class with instant cache + async persistence, and the low-level `UserDefaults` class for direct key-value access.

---

## Settings Class

`Settings` is the recommended way to manage application preferences. It provides instant reads from an in-memory cache and automatic background writes to macOS UserDefaults.

### Defining settings

Create a `Settings` object with a dictionary of defaults, then register it with the app:

```python
import nib

def main(app: nib.App):
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
        "username": "",
        "volume": 50,
    })

    app.register_settings(settings)

    # Read immediately -- returns cached value
    print(f"Dark mode: {settings.dark_mode}")
    print(f"Font size: {settings.font_size}")

    # Write -- updates cache instantly, persists in background
    settings.dark_mode = True
    settings.volume = 75

    app.build(nib.Text("Settings loaded", padding=24))

nib.run(main)
```

### How it works

1. On `register_settings()`, Nib loads any previously saved values from UserDefaults into the cache.
2. Reading a setting (e.g., `settings.dark_mode`) returns the cached value instantly -- no blocking I/O.
3. Writing a setting (e.g., `settings.dark_mode = True`) updates the cache and sends a fire-and-forget write to UserDefaults.

!!! info
    The first `register_settings()` call blocks briefly (up to 2 seconds) while loading saved values. After that, all reads and writes are non-blocking.

### on_load callback

If you need to run code after settings have loaded from UserDefaults, use the `on_load` callback:

```python
def on_settings_loaded():
    print("Settings loaded from disk")
    theme_label.content = settings.theme

settings = nib.Settings(
    {"theme": "light", "auto_save": True},
    on_load=on_settings_loaded,
)
app.register_settings(settings)
```

### Reset to defaults

```python
# Reset a single setting
settings.reset("font_size")

# Reset all settings
settings.reset()
```

### Get all settings as a dict

```python
all_settings = settings.to_dict()
# {"dark_mode": True, "font_size": 14, "username": "", "volume": 75}
```

---

## Settings-Driven UI

Use settings to drive your UI. When a control changes, update the setting. When the app loads, read the setting to set the initial state.

```python
import nib

def main(app: nib.App):
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
        "notifications": True,
    })
    app.register_settings(settings)

    # Build UI driven by settings
    dark_toggle = nib.Toggle(
        "Dark Mode",
        is_on=settings.dark_mode,
        on_change=lambda is_on: setattr(settings, "dark_mode", is_on),
    )

    font_slider = nib.Slider(
        "Font Size",
        value=settings.font_size,
        min_value=10,
        max_value=24,
        on_change=lambda val: setattr(settings, "font_size", int(val)),
    )

    notify_toggle = nib.Toggle(
        "Notifications",
        is_on=settings.notifications,
        on_change=lambda is_on: setattr(settings, "notifications", is_on),
    )

    app.build(
        nib.Form(
            controls=[
                nib.Section(
                    controls=[dark_toggle, font_slider],
                    header="Appearance",
                ),
                nib.Section(
                    controls=[notify_toggle],
                    header="Alerts",
                ),
            ],
            style=nib.FormStyle.GROUPED,
            padding=16,
        )
    )

nib.run(main)
```

---

## Settings Page with Tabs

For a native macOS preferences window, create a `SettingsPage` with one or more `SettingsTab` items and assign it to `app.settings`.

```python
import nib

def main(app: nib.App):
    app.title = "Preferences App"
    app.icon = nib.SFSymbol("gear")
    app.width = 300
    app.height = 200

    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
        "auto_update": True,
    })
    app.register_settings(settings)

    app.settings = nib.SettingsPage(
        width=500,
        height=400,
        title="Preferences",
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.Form(
                    controls=[
                        nib.Toggle("Dark Mode", is_on=settings.dark_mode,
                                   on_change=lambda v: setattr(settings, "dark_mode", v)),
                        nib.Slider("Font Size", value=settings.font_size,
                                   min_value=10, max_value=24,
                                   on_change=lambda v: setattr(settings, "font_size", int(v))),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
            nib.SettingsTab(
                "Updates",
                icon="arrow.triangle.2.circlepath",
                content=nib.Form(
                    controls=[
                        nib.Toggle("Auto-Update", is_on=settings.auto_update,
                                   on_change=lambda v: setattr(settings, "auto_update", v)),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
        ],
    )

    # Open settings from a button
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Preferences App", font=nib.Font.HEADLINE),
                nib.Button("Open Settings", action=app.settings.open),
            ],
            spacing=12,
            padding=24,
        )
    )

nib.run(main)
```

### Opening the settings window

- Programmatically: call `app.settings.open()`
- Keyboard shortcut: `Cmd+,` (automatically wired when `app.settings` is set)
- From a menu item: `nib.MenuItem("Settings", action=app.settings.open, icon="gear", shortcut="cmd,,")`

### SettingsTab parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | `str` | Tab title shown in the tab bar |
| `icon` | `str` | SF Symbol name for the tab icon |
| `content` | `View` | The view displayed when the tab is selected |

### SettingsPage parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tabs` | `list[SettingsTab]` | `[]` | List of tabs |
| `content` | `View` | `None` | Single view (creates one "General" tab) |
| `width` | `float` | `450` | Window width |
| `height` | `float` | `300` | Window height |
| `title` | `str` | `"Settings"` | Window title |

---

## UserDefaults -- Low-Level Access

For direct key-value persistence without the Settings wrapper, use `UserDefaults`. All reads are blocking with a configurable timeout.

```python
import nib

def main(app: nib.App):
    app.title = "UserDefaults Demo"
    app.icon = nib.SFSymbol("cylinder.split.1x2")
    app.width = 300
    app.height = 200

    defaults = nib.UserDefaults()

    # Write values (fire-and-forget)
    defaults.set("username", "john_doe")
    defaults.set("login_count", 42)
    defaults.set("dark_mode", True)
    defaults.set("tags", ["python", "swift"])

    # Read values (blocking, up to 5s timeout)
    username = defaults.get("username", default="guest")
    count = defaults.get("login_count", default=0)

    # Check existence
    if defaults.contains_key("api_token"):
        token = defaults.get("api_token")

    # Get all keys with a prefix
    settings_keys = defaults.get_keys("settings.")

    # Remove a key
    defaults.remove("old_key")

    # Clear all keys
    # defaults.clear()

    app.build(
        nib.VStack(
            controls=[
                nib.Text(f"User: {username}", font=nib.Font.HEADLINE),
                nib.Text(f"Logins: {count}"),
            ],
            spacing=8,
            padding=24,
        )
    )

nib.run(main)
```

### Supported value types

| Python Type | Stored As |
|-------------|-----------|
| `str` | String |
| `int` | Integer |
| `float` | Float |
| `bool` | Boolean |
| `list` | JSON array |
| `dict` | JSON dictionary |
| `bytes` | Base64-encoded data |

!!! warning
    `UserDefaults.get()` is a blocking call that waits for a round trip to the Swift runtime. Use `Settings` for performance-sensitive reads.
