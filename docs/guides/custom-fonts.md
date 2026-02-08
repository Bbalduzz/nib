# Custom Fonts

Nib supports loading custom font files for use in your views. Fonts can be auto-detected from the assets directory, registered manually by path, or loaded from a URL.

## Auto-detection from assets

The simplest approach is to place font files in your `assets/` directory. Nib scans for font files automatically before the first render:

```
myapp/
├── src/
│   ├── main.py
│   └── assets/
│       ├── Geist-Regular.ttf
│       ├── Geist-Bold.ttf
│       └── FiraCode-Regular.otf
```

Font files are detected by extension. Supported formats:

| Extension | Format |
|-----------|--------|
| `.ttf` | TrueType |
| `.otf` | OpenType |
| `.ttc` | TrueType Collection |
| `.woff` | Web Open Font Format |
| `.woff2` | Web Open Font Format 2 |

### Font naming

The font name is derived from the filename without its extension. For example:

| Filename | Font name |
|----------|-----------|
| `Geist-Regular.ttf` | `Geist-Regular` |
| `FiraCode-Medium.otf` | `FiraCode-Medium` |
| `Inter-Bold.ttf` | `Inter-Bold` |

### Subdirectory scanning

Nib scans the assets directory recursively, so you can organize fonts in subdirectories:

```
assets/
├── fonts/
│   ├── Geist-Regular.ttf
│   └── Geist-Bold.ttf
└── images/
    └── logo.png
```

Both fonts will be detected and available by their filename-based names.

## Manual registration

For fonts outside the assets directory, register them explicitly with `app.fonts`:

```python
app.fonts = {
    "MyCustomFont": "/absolute/path/to/MyCustomFont.ttf",
    "AnotherFont": "/Users/me/Library/Fonts/AnotherFont.otf",
}
```

The dictionary maps font names (used in code) to absolute file paths.

### URL-based fonts

You can also load fonts from a URL:

```python
app.fonts = {
    "WebFont": "https://example.com/fonts/WebFont.ttf",
}
```

The Swift runtime downloads and caches the font at startup.

### Combining auto-detection and manual registration

Manual registrations are merged with auto-detected fonts. If there is a name conflict, the manual registration takes precedence:

```python
# Auto-detected fonts from assets/ are available automatically.
# These manual entries are added on top:
app.fonts = {
    "Geist-Regular": "/path/to/override/Geist-Regular.ttf",  # overrides auto-detected
    "ExternalFont": "/other/path/ExternalFont.otf",           # new font
}
```

## Using custom fonts

Once registered (automatically or manually), use `nib.Font.custom()` to reference a custom font:

```python
nib.Text("Hello, World!", font=nib.Font.custom("Geist-Regular", size=16))
```

The first argument is the font name (matching the registered name), and `size` is the point size.

### In different views

Custom fonts work anywhere a `font` parameter is accepted:

```python
# Text
nib.Text("Custom styled text", font=nib.Font.custom("FiraCode-Regular", size=14))

# TextField
nib.TextField(value="", placeholder="Type here", font=nib.Font.custom("Inter-Bold", size=14))

# Button
nib.Button(
    content=nib.Text("Click Me", font=nib.Font.custom("Geist-Bold", size=16)),
    action=on_click,
)
```

### On Canvas

Custom fonts work with the `nib.draw.Text` command as well:

```python
canvas.draw([
    nib.draw.Text(
        "Canvas text",
        x=10, y=50,
        font=nib.Font.custom("Geist-Regular", size=20),
        fill="#ffffff",
    ),
])
```

## Font loading order

Font discovery and registration happens in this order:

1. Nib auto-detects font files in the `assets/` directory (recursively).
2. Manually registered fonts via `app.fonts` are merged in, overriding any auto-detected fonts with the same name.
3. The combined font dictionary is sent to the Swift runtime on the first render.
4. Swift loads and registers all fonts before displaying the UI.

!!! note
    Font loading happens once, before the first render. If you update `app.fonts` after the app is running, the new fonts will be sent on the next re-render.

## Complete example

```python
import nib


def main(app: nib.App):
    app.title = "Fonts"
    app.icon = nib.SFSymbol("textformat")
    app.width = 350
    app.height = 350

    # Manual registration (auto-detection from assets/ also works)
    app.fonts = {
        "Geist-Regular": "/Users/me/fonts/Geist-Regular.ttf",
        "Geist-Bold": "/Users/me/fonts/Geist-Bold.ttf",
    }

    app.build(
        nib.VStack(
            controls=[
                nib.Text("System Font", font=nib.Font.TITLE),
                nib.Divider(),
                nib.Text(
                    "Custom Regular",
                    font=nib.Font.custom("Geist-Regular", size=18),
                ),
                nib.Text(
                    "Custom Bold",
                    font=nib.Font.custom("Geist-Bold", size=18),
                ),
                nib.Divider(),
                nib.Text(
                    "Small custom font",
                    font=nib.Font.custom("Geist-Regular", size=12),
                    foreground_color=nib.Color.GRAY,
                ),
                nib.Text(
                    "Large custom font",
                    font=nib.Font.custom("Geist-Bold", size=28),
                ),
            ],
            spacing=12,
            padding=24,
        )
    )


nib.run(main)
```

!!! tip
    For the best developer experience, place font files in `assets/` and let auto-detection handle everything. You only need manual registration for fonts stored outside your project directory or loaded from URLs.
