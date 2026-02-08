# Screen

The Screen service provides access to display information and control, including brightness, resolution, dark mode, screenshots, and multi-display management. Access it via `app.screen`.

```python
info = app.screen.get_info()
print(f"Display: {info.name}")
print(f"Resolution: {info.width}x{info.height} @{info.scale}x")
```

## Methods

### `get_info()`

Get information about the current display, including brightness, dimensions, refresh rate, color space, and native resolution.

```python
app.screen.get_info() -> ScreenInfo
```

Returns a `ScreenInfo` dataclass.

### `list_displays()`

List all connected displays with their properties.

```python
app.screen.list_displays() -> list[dict]
```

Returns a list of dictionaries, each containing:

| Key | Type | Description |
|-----|------|-------------|
| `index` | `int` | Display index |
| `displayID` | `int` | System display ID |
| `name` | `str` | Display name (e.g., `"Built-in Retina Display"`) |
| `width` | `float` | Resolution width in points |
| `height` | `float` | Resolution height in points |
| `scale` | `float` | Scale factor (e.g., `2.0` for Retina) |
| `isMain` | `bool` | Whether this is the main display |
| `isBuiltin` | `bool` | Whether this is the built-in display |
| `refreshRate` | `float` | Refresh rate in Hz |
| `colorSpace` | `str` | Color space name |

### `set_brightness(brightness)`

Set the screen brightness. Only works on built-in displays.

```python
app.screen.set_brightness(brightness: float) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `brightness` | `float` | Brightness level from `0.0` (darkest) to `1.0` (brightest). Values are clamped to this range. |

Returns `True` if brightness was set successfully.

### `set_resolution(width, height)`

Change the screen resolution. The target resolution must be one of the available modes from `get_info().available_resolutions`.

```python
app.screen.set_resolution(width: int, height: int) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Target width in points |
| `height` | `int` | Target height in points |

Returns `True` if the resolution was changed successfully.

### `get_dark_mode()`

Get the current dark mode status.

```python
app.screen.get_dark_mode() -> DarkModeInfo
```

Returns a `DarkModeInfo` dataclass.

### `set_dark_mode(enabled)`

Toggle system dark mode. Requires automation permission for System Events.

```python
app.screen.set_dark_mode(enabled: bool) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | `bool` | `True` for dark mode, `False` for light mode |

Returns `True` if the change was applied successfully.

### `get_color_profile()`

Get the current color profile information.

```python
app.screen.get_color_profile() -> ColorProfileInfo
```

Returns a `ColorProfileInfo` dataclass.

### `screenshot(display_id, x, y, width, height)`

Capture a screenshot of the full screen or a specified region. Requires screen recording permission.

```python
app.screen.screenshot(
    display_id: int | None = None,
    x: float | None = None,
    y: float | None = None,
    width: float | None = None,
    height: float | None = None,
) -> ScreenshotResult
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `display_id` | `int \| None` | `None` | Specific display ID. Uses the main display if `None` |
| `x` | `float \| None` | `None` | X origin of the capture region |
| `y` | `float \| None` | `None` | Y origin of the capture region |
| `width` | `float \| None` | `None` | Width of the capture region |
| `height` | `float \| None` | `None` | Height of the capture region |

All four region parameters (`x`, `y`, `width`, `height`) must be provided together or omitted entirely for a full-screen capture.

Returns a `ScreenshotResult` dataclass.

---

## Data Classes

### `ScreenInfo`

Display information returned by `get_info()`.

| Property | Type | Description |
|----------|------|-------------|
| `brightness` | `float \| None` | Current brightness level (0.0--1.0). `None` if unavailable |
| `is_builtin` | `bool` | Whether this is the built-in display |
| `width` | `float` | Screen width in points |
| `height` | `float` | Screen height in points |
| `scale` | `float` | Display scale factor (e.g., `2.0` for Retina) |
| `visible_width` | `float \| None` | Visible width excluding dock and menu bar |
| `visible_height` | `float \| None` | Visible height excluding dock and menu bar |
| `display_id` | `int \| None` | System display identifier |
| `name` | `str \| None` | Display name (e.g., `"Built-in Retina Display"`) |
| `refresh_rate` | `float \| None` | Display refresh rate in Hz |
| `native_width` | `int \| None` | Native pixel width |
| `native_height` | `int \| None` | Native pixel height |
| `color_space` | `str \| None` | Color space name |
| `color_depth` | `int \| None` | Bits per pixel |
| `available_resolutions` | `list[dict]` | List of available display modes |

### `DarkModeInfo`

Dark mode information returned by `get_dark_mode()`.

| Property | Type | Description |
|----------|------|-------------|
| `is_dark_mode` | `bool` | Whether dark mode is currently enabled |
| `appearance_name` | `str \| None` | Full appearance name (e.g., `"NSAppearanceNameDarkAqua"`) |

### `ColorProfileInfo`

Color profile information returned by `get_color_profile()`.

| Property | Type | Description |
|----------|------|-------------|
| `color_space_name` | `str \| None` | Color space name |
| `color_component_count` | `int \| None` | Number of color components |
| `icc_profile_size` | `int \| None` | Size of ICC profile in bytes |

### `ScreenshotResult`

Screenshot result returned by `screenshot()`.

| Property | Type | Description |
|----------|------|-------------|
| `success` | `bool` | Whether the screenshot was captured successfully |
| `image_data` | `bytes \| None` | Raw PNG image data |
| `width` | `int \| None` | Image width in pixels |
| `height` | `int \| None` | Image height in pixels |

#### `ScreenshotResult.save(path)`

Save the screenshot to a file.

```python
result.save(path: str) -> bool
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `str` | File path to save to (should end in `.png`) |

Returns `True` if saved successfully, `False` if the screenshot was not captured or an I/O error occurred.

---

## Examples

### Display information dashboard

```python
import nib

def main(app: nib.App):
    app.title = "Display"
    app.icon = nib.SFSymbol("display")
    app.width = 320
    app.height = 250

    name_text = nib.Text("--", font=nib.Font.HEADLINE)
    res_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    brightness_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)
    refresh_text = nib.Text("--", foreground_color=nib.Color.SECONDARY)

    def refresh():
        info = app.screen.get_info()
        name_text.content = info.name or "Display"
        res_text.content = f"{info.width:.0f} x {info.height:.0f} @{info.scale:.0f}x"
        brightness_text.content = (
            f"Brightness: {info.brightness * 100:.0f}%"
            if info.brightness is not None
            else "Brightness: N/A"
        )
        refresh_text.content = (
            f"Refresh rate: {info.refresh_rate:.0f} Hz"
            if info.refresh_rate
            else "Refresh rate: N/A"
        )

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[name_text, res_text, brightness_text, refresh_text],
            spacing=8,
            padding=20,
        )
    )

nib.run(main)
```

### Brightness slider

```python
import nib

def main(app: nib.App):
    app.title = "Brightness"
    app.icon = nib.SFSymbol("sun.max")
    app.width = 300
    app.height = 120

    label = nib.Text("50%")

    def on_change(value):
        app.screen.set_brightness(value / 100)
        label.content = f"{value:.0f}%"

    def load_current():
        info = app.screen.get_info()
        if info.brightness is not None:
            label.content = f"{info.brightness * 100:.0f}%"

    app.on_appear = load_current

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Slider(value=50, min_value=0, max_value=100, on_change=on_change),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Dark mode toggle

```python
import nib

def main(app: nib.App):
    app.title = "Appearance"
    app.icon = nib.SFSymbol("moon.fill")
    app.width = 280
    app.height = 100

    mode_text = nib.Text("--", font=nib.Font.HEADLINE)

    def refresh():
        info = app.screen.get_dark_mode()
        mode_text.content = "Dark Mode" if info.is_dark_mode else "Light Mode"

    def toggle():
        info = app.screen.get_dark_mode()
        app.screen.set_dark_mode(not info.is_dark_mode)
        refresh()

    app.on_appear = refresh

    app.build(
        nib.VStack(
            controls=[
                mode_text,
                nib.Button("Toggle", action=toggle, style=nib.ButtonStyle.BORDERED),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Take a screenshot

```python
import nib

def main(app: nib.App):
    app.title = "Screenshot"
    app.icon = nib.SFSymbol("camera.viewfinder")
    app.width = 300
    app.height = 120

    status = nib.Text("Ready", foreground_color=nib.Color.SECONDARY)

    def capture():
        result = app.screen.screenshot()
        if result.success:
            saved = result.save("/tmp/nib_screenshot.png")
            if saved:
                status.content = f"Saved {result.width}x{result.height} screenshot"
            else:
                status.content = "Failed to save screenshot"
        else:
            status.content = "Screenshot capture failed"

    app.build(
        nib.VStack(
            controls=[
                nib.Button("Capture Screenshot", action=capture),
                status,
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```
