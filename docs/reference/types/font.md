# Font

The `Font` dataclass configures typography for text views. It supports system semantic fonts, custom font sizes, custom font families, and font file loading.

```python
import nib

# System semantic font
title = nib.Text("Welcome", font=nib.Font.TITLE)

# Custom size with weight
label = nib.Text("Label", font=nib.Font.system(14, nib.FontWeight.MEDIUM))

# Custom font family from file
code = nib.Text("code", font=nib.Font.custom("Iosevka", 13, path="fonts/Iosevka.ttf"))
```

## System Fonts

System fonts use Apple's semantic sizing, which adapts to accessibility and platform settings.

| Constant | Description |
|----------|-------------|
| `Font.LARGE_TITLE` | Large title text (largest semantic size) |
| `Font.TITLE` | Title text |
| `Font.TITLE2` | Secondary title text |
| `Font.TITLE3` | Tertiary title text |
| `Font.HEADLINE` | Headline text (semibold by default) |
| `Font.SUBHEADLINE` | Subheadline text |
| `Font.BODY` | Body text (default reading size) |
| `Font.CALLOUT` | Callout text (slightly smaller than body) |
| `Font.FOOTNOTE` | Footnote text |
| `Font.CAPTION` | Caption text |
| `Font.CAPTION2` | Secondary caption text (smallest semantic size) |

```python
nib.Text("Title", font=nib.Font.TITLE)
nib.Text("Body text", font=nib.Font.BODY)
nib.Text("Fine print", font=nib.Font.CAPTION)
```

## Factory Methods

### `Font.system(size, weight=None)`

Create a system font with a specific point size and optional weight.

```python
font = nib.Font.system(18)
font = nib.Font.system(16, nib.FontWeight.BOLD)
font = nib.Font.system(14, "semibold")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `float` | -- | Font size in points. |
| `weight` | `FontWeight \| str` | `None` | Optional font weight. |

### `Font.custom(name, size, weight=None, path=None)`

Create a custom font by family name. Optionally provide a path to a `.ttf` or `.otf` file for runtime font loading.

```python
# System-installed font
font = nib.Font.custom("Helvetica Neue", 16)

# Font from a bundled file
font = nib.Font.custom("Inter", 14, weight=nib.FontWeight.MEDIUM, path="fonts/Inter.ttf")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Font family name (e.g., `"Inter"`, `"Roboto"`). |
| `size` | `float` | -- | Font size in points. |
| `weight` | `FontWeight \| str` | `None` | Optional font weight. |
| `path` | `str` | `None` | Path to `.ttf` or `.otf` file for runtime loading. |

## FontWeight

The `FontWeight` enum specifies text thickness. It can be used with `Font.system()`, `Font.custom()`, or the `font_weight` view modifier parameter.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `FontWeight.ULTRA_LIGHT` | `.ultraLight` | Thinnest weight |
| `FontWeight.THIN` | `.thin` | Very thin |
| `FontWeight.LIGHT` | `.light` | Light weight |
| `FontWeight.REGULAR` | `.regular` | Standard weight (default) |
| `FontWeight.MEDIUM` | `.medium` | Medium weight |
| `FontWeight.SEMIBOLD` | `.semibold` | Semi-bold weight |
| `FontWeight.BOLD` | `.bold` | Bold weight |
| `FontWeight.HEAVY` | `.heavy` | Heavy weight |
| `FontWeight.BLACK` | `.black` | Heaviest weight |

```python
nib.Text("Light", font_weight=nib.FontWeight.LIGHT)
nib.Text("Bold", font_weight=nib.FontWeight.BOLD)
nib.Text("Heavy", font=nib.Font.system(20, nib.FontWeight.HEAVY))
```

## String Shortcut

When a string is passed to the `font` parameter, it is treated as a font family name.

```python
# These are equivalent:
nib.Text("Hello", font=nib.Font.custom("Helvetica Neue", 16))
nib.Text("Hello", font="Helvetica Neue")
```

Note that the string shortcut does not allow specifying a size -- the system default size is used. Use `Font.custom()` when you need to control the size.

## Examples

### Combining font and weight

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Large Title", font=nib.Font.LARGE_TITLE),
                nib.Text("Bold Headline", font=nib.Font.HEADLINE, font_weight=nib.FontWeight.BOLD),
                nib.Text("Custom Size", font=nib.Font.system(22, nib.FontWeight.SEMIBOLD)),
                nib.Text("Caption", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Loading a custom font file

```python
import nib

mono_font = nib.Font.custom("JetBrains Mono", 13, path="fonts/JetBrainsMono-Regular.ttf")

def main(app: nib.App):
    app.build(
        nib.Text("fn main() { println!(\"Hello\"); }", font=mono_font)
    )

nib.run(main)
```
