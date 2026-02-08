# Typography Modifiers

Typography modifiers control the font and weight of text content within views. They map to SwiftUI's `.font()` view modifier.

```python
import nib

nib.Text("Title", font=nib.Font.TITLE, font_weight=nib.FontWeight.BOLD)
```

---

## font

Configures the font for text content. Accepts a `Font` object or a font family name string.

| Type | Default |
|------|---------|
| `Font \| str` | `None` |

### Using system fonts

System fonts use Apple's semantic sizing, which adapts to accessibility settings:

```python
nib.Text("Title", font=nib.Font.TITLE)
nib.Text("Body", font=nib.Font.BODY)
nib.Text("Caption", font=nib.Font.CAPTION)
```

See [Font](../types/font.md) for all system font constants.

### Using custom sizes

Create a font with a specific point size:

```python
nib.Text("Custom", font=nib.Font.system(18))
nib.Text("Bold Custom", font=nib.Font.system(20, nib.FontWeight.BOLD))
```

### Using font family names

Pass a string to use a named font family:

```python
nib.Text("Helvetica", font="Helvetica Neue")
```

### Using custom font files

Load a font from a `.ttf` or `.otf` file:

```python
nib.Text("Custom", font=nib.Font.custom("Inter", 14, path="fonts/Inter.ttf"))
```

### Font with weight embedded

The `Font.system()` and `Font.custom()` methods accept an optional weight parameter:

```python
nib.Text("Heavy", font=nib.Font.system(24, nib.FontWeight.HEAVY))
nib.Text("Light Custom", font=nib.Font.custom("Inter", 16, weight=nib.FontWeight.LIGHT))
```

---

## font_weight

Sets the font weight independently. This can be used alone or in combination with `font`. When both `font` (with a weight) and `font_weight` are specified, `font_weight` takes precedence.

| Type | Default |
|------|---------|
| `FontWeight \| str` | `None` |

```python
nib.Text("Bold", font_weight=nib.FontWeight.BOLD)
nib.Text("Semibold", font_weight="semibold")
nib.Text("Light", font_weight=nib.FontWeight.LIGHT)
```

### FontWeight values

| Value | Description |
|-------|-------------|
| `FontWeight.ULTRA_LIGHT` | Thinnest weight |
| `FontWeight.THIN` | Very thin |
| `FontWeight.LIGHT` | Light |
| `FontWeight.REGULAR` | Standard (default) |
| `FontWeight.MEDIUM` | Medium |
| `FontWeight.SEMIBOLD` | Semi-bold |
| `FontWeight.BOLD` | Bold |
| `FontWeight.HEAVY` | Heavy |
| `FontWeight.BLACK` | Heaviest weight |

### Combining font and font_weight

```python
# font_weight overrides the weight in the Font object
nib.Text(
    "Override",
    font=nib.Font.system(18, nib.FontWeight.LIGHT),
    font_weight=nib.FontWeight.BOLD,  # This takes precedence
)
```

## Examples

### Typography scale

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Large Title", font=nib.Font.LARGE_TITLE),
                nib.Text("Title", font=nib.Font.TITLE),
                nib.Text("Headline", font=nib.Font.HEADLINE),
                nib.Text("Body", font=nib.Font.BODY),
                nib.Text("Callout", font=nib.Font.CALLOUT),
                nib.Text("Footnote", font=nib.Font.FOOTNOTE),
                nib.Text("Caption", font=nib.Font.CAPTION),
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=4,
            padding=16,
        )
    )

nib.run(main)
```

### Mixed fonts in a layout

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Dashboard", font=nib.Font.LARGE_TITLE, font_weight=nib.FontWeight.BOLD),
                nib.HStack(
                    controls=[
                        nib.Text("Status:", font=nib.Font.BODY),
                        nib.Text("Active", font_weight=nib.FontWeight.SEMIBOLD, foreground_color=nib.Color.GREEN),
                    ],
                    spacing=4,
                ),
                nib.Text(
                    "Last updated: just now",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.SECONDARY,
                ),
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
