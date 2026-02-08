# Settings

Application settings manager with instant reads from a local cache and automatic background persistence to macOS UserDefaults. Provides attribute-style access via dot notation.

## Constructor

```python
nib.Settings(defaults: dict[str, Any], on_load: Callable[[], None] | None = None)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `defaults` | `dict[str, Any]` | -- | Dictionary mapping setting names to their default values. These defaults are used when no saved value exists in UserDefaults |
| `on_load` | `Callable[[], None] \| None` | `None` | Optional callback invoked when settings finish loading persisted values from UserDefaults |

## Properties

| Property | Type | Description |
|---|---|---|
| `on_load` | `Callable[[], None] \| None` | Get or set the callback invoked when settings finish loading. If settings have already loaded, assigning a new callback invokes it immediately |
| `<setting_name>` | `Any` | Any key defined in `defaults` is accessible as an attribute. Reading returns the cached value instantly; writing updates the cache and persists in the background |

## Methods

### `get(name, default)`

Get a setting value with an optional fallback.

```python
settings.get(name: str, default: Any = None) -> Any
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | -- | The setting name |
| `default` | `Any` | `None` | Value returned if the setting is not found |

### `set(name, value)`

Set a setting value. Alternative to attribute assignment.

```python
settings.set(name: str, value: Any) -> None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | -- | The setting name (must be defined in `defaults`) |
| `value` | `Any` | -- | The new value |

### `wait_for_load(timeout)`

Block until initial settings have been loaded from UserDefaults. Usually not needed since defaults are available immediately.

```python
settings.wait_for_load(timeout: float = 5.0) -> bool
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `timeout` | `float` | `5.0` | Maximum wait time in seconds |

**Returns:** `True` if loading completed, `False` if timed out.

### `load(blocking, timeout)`

Trigger loading of persisted values from UserDefaults. Called automatically on first attribute access, but can be called explicitly for more control.

```python
settings.load(blocking: bool = False, timeout: float = 2.0) -> None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `blocking` | `bool` | `False` | If `True`, waits for the load to complete before returning |
| `timeout` | `float` | `2.0` | Maximum wait time when `blocking=True` |

### `to_dict()`

Get all current settings as a plain dictionary.

```python
settings.to_dict() -> dict[str, Any]
```

### `reset(name)`

Reset settings to their default values.

```python
settings.reset(name: str | None = None) -> None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str \| None` | `None` | Specific setting to reset. If `None`, resets all settings to defaults |

## How It Works

1. **Cache layer**: All reads go to an in-memory dictionary, so `settings.dark_mode` never blocks.
2. **Background persistence**: Writes update the cache immediately, then fire-and-forget a message to the Swift runtime to persist in UserDefaults.
3. **Initial load**: When registered with `app.register_settings()`, saved values are loaded from UserDefaults in a background thread and merged into the cache. The `on_load` callback fires when this completes.
4. **Attribute validation**: Only keys defined in `defaults` can be read or written. Accessing an undefined key raises `AttributeError`.

## Examples

### Basic settings with persistence

```python
import nib

def main(app: nib.App):
    app.title = "Preferences Demo"
    app.icon = nib.SFSymbol("gear")
    app.width = 350
    app.height = 250

    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
        "username": "guest",
    })
    app.register_settings(settings)

    status = nib.Text(f"User: {settings.username}, Font: {settings.font_size}pt")

    def toggle_dark():
        settings.dark_mode = not settings.dark_mode
        status.content = f"Dark mode: {settings.dark_mode}"

    app.build(
        nib.VStack(
            controls=[
                status,
                nib.Button("Toggle Dark Mode", action=toggle_dark),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Using on_load to update UI after persisted values load

```python
import nib

def main(app: nib.App):
    app.title = "Settings"
    app.icon = nib.SFSymbol("slider.horizontal.3")
    app.width = 350
    app.height = 200

    label = nib.Text("Loading...", font=nib.Font.HEADLINE)

    settings = nib.Settings(
        {"volume": 50, "notifications": True},
        on_load=lambda: setattr(label, "content", f"Volume: {settings.volume}%"),
    )
    app.register_settings(settings)

    def update_volume(value):
        settings.volume = int(value)
        label.content = f"Volume: {settings.volume}%"

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Slider(
                    "Volume",
                    value=settings.volume,
                    min_value=0,
                    max_value=100,
                    on_change=update_volume,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Resetting settings

```python
import nib

def main(app: nib.App):
    app.title = "Reset Demo"
    app.icon = nib.SFSymbol("arrow.counterclockwise")
    app.width = 300
    app.height = 150

    settings = nib.Settings({"theme": "light", "volume": 50})
    app.register_settings(settings)

    info = nib.Text(f"Theme: {settings.theme}, Volume: {settings.volume}")

    def reset_all():
        settings.reset()
        info.content = f"Theme: {settings.theme}, Volume: {settings.volume}"

    def reset_theme():
        settings.reset("theme")
        info.content = f"Theme: {settings.theme}, Volume: {settings.volume}"

    app.build(
        nib.VStack(
            controls=[
                info,
                nib.Button("Reset Theme", action=reset_theme),
                nib.Button("Reset All", action=reset_all),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

## Related

- [App](app.md) -- Register settings via `app.register_settings()`
- [UserDefaults](user-defaults.md) -- Low-level persistent storage used under the hood
- [SettingsPage](settings-page.md) -- UI for a preferences window
