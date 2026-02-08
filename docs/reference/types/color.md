# Color

The `Color` dataclass represents color values for styling views. Colors can be defined using predefined constants, hex strings, RGB values, or named system colors.

```python
import nib

# Predefined color
text = nib.Text("Hello", foreground_color=nib.Color.BLUE)

# Hex color
box = nib.Rectangle(fill=nib.Color(hex="#4287f5"))

# RGB color
accent = nib.Color.rgb(66, 135, 245)
```

## Constructor

```python
Color(value=None, *, hex=None, opacity=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `str` | `None` | Named color string (e.g., `"red"`, `"blue"`). Used internally by predefined constants. |
| `hex` | `str` | `None` | Hex color string. Accepts `"#4287f5"` or `"4287f5"` (the `#` prefix is added automatically). Supports ARGB alpha channel: `"#7fff6666"`. |
| `opacity` | `float` | `None` | Opacity from `0.0` (fully transparent) to `1.0` (fully opaque). |

Either `value` or `hex` must be provided. A `ValueError` is raised if neither is given.

## Class Methods

### `Color.hex(hex_value)`

Create a color from a hex string.

```python
color = nib.Color.hex("#4287f5")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `hex_value` | `str` | Hex color string, with or without `#` prefix. |

### `Color.rgb(r, g, b)`

Create a color from RGB values in the 0--255 range.

```python
color = nib.Color.rgb(66, 135, 245)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `r` | `int` | Red component (0--255). |
| `g` | `int` | Green component (0--255). |
| `b` | `int` | Blue component (0--255). |

### `Color.rgba(r, g, b, a)`

Create a color from RGBA values. RGB components are 0--255, alpha is 0.0--1.0.

```python
color = nib.Color.rgba(66, 135, 245, 0.8)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `r` | `int` | Red component (0--255). |
| `g` | `int` | Green component (0--255). |
| `b` | `int` | Blue component (0--255). |
| `a` | `float` | Alpha/opacity (0.0--1.0). |

## Instance Methods

### `color.with_opacity(opacity)`

Return a new `Color` with the specified opacity. The original color is not modified.

```python
faded_blue = nib.Color.BLUE.with_opacity(0.5)
custom = nib.Color(hex="#FF5733").with_opacity(0.3)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `opacity` | `float` | Opacity from `0.0` to `1.0`. |

## Predefined Colors

### Basic Colors

| Constant | Value | Description |
|----------|-------|-------------|
| `Color.RED` | `"red"` | System red |
| `Color.BLUE` | `"blue"` | System blue |
| `Color.GREEN` | `"green"` | System green |
| `Color.YELLOW` | `"yellow"` | System yellow |
| `Color.ORANGE` | `"orange"` | System orange |
| `Color.PINK` | `"pink"` | System pink |
| `Color.PURPLE` | `"purple"` | System purple |
| `Color.CYAN` | `"cyan"` | System cyan |
| `Color.WHITE` | `"white"` | White |
| `Color.BLACK` | `"black"` | Black |
| `Color.GRAY` | `"gray"` | System gray |
| `Color.CLEAR` | `"clear"` | Fully transparent |

### Extended Colors

| Constant | Value | Description |
|----------|-------|-------------|
| `Color.INDIGO` | `"indigo"` | System indigo |
| `Color.MINT` | `"mint"` | System mint |
| `Color.TEAL` | `"teal"` | System teal |
| `Color.BROWN` | `"brown"` | System brown |

### Semantic Colors

| Constant | Value | Description |
|----------|-------|-------------|
| `Color.PRIMARY` | `"primary"` | Primary label color (adapts to light/dark mode) |
| `Color.SECONDARY` | `"secondary"` | Secondary label color (adapts to light/dark mode) |
| `Color.ACCENT` | `"accentColor"` | System accent color |

## String Shortcuts

Anywhere a `Color` is accepted, you can also pass a plain string. Nib resolves named color strings and hex strings automatically.

```python
# These are equivalent:
nib.Text("Hello", foreground_color=nib.Color.RED)
nib.Text("Hello", foreground_color="red")

# Hex strings work too:
nib.Text("Hello", foreground_color="#FF5733")
nib.Rectangle(fill="#262626", stroke="#383837")
```

## Examples

### Combining colors with opacity

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Solid", foreground_color=nib.Color.BLUE),
                nib.Text("Faded", foreground_color=nib.Color.BLUE.with_opacity(0.4)),
                nib.Rectangle(
                    fill=nib.Color.rgba(255, 100, 50, 0.6),
                    width=100,
                    height=50,
                ),
            ],
            spacing=8,
        )
    )

nib.run(main)
```

### Using hex colors for custom themes

```python
import nib

DARK_BG = nib.Color(hex="#1E1E2E")
SURFACE = nib.Color(hex="#313244")
TEXT_PRIMARY = nib.Color(hex="#CDD6F4")
ACCENT = nib.Color(hex="#89B4FA")

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Dashboard", font=nib.Font.TITLE, foreground_color=TEXT_PRIMARY),
                nib.Text("Welcome back", foreground_color=ACCENT),
            ],
            spacing=12,
            padding=20,
            background=DARK_BG,
        )
    )

nib.run(main)
```
