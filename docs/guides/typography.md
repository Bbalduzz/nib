# Typography & Fonts

Nib gives you access to the full set of SwiftUI system fonts, custom size and weight control, custom font files, and rich text with attributed strings.

---

## System Fonts

System fonts are predefined on the `Font` class and match the macOS Dynamic Type styles:

```python
import nib

nib.Text("Large Title", font=nib.Font.LARGE_TITLE)
nib.Text("Title", font=nib.Font.TITLE)
nib.Text("Title 2", font=nib.Font.TITLE2)
nib.Text("Title 3", font=nib.Font.TITLE3)
nib.Text("Headline", font=nib.Font.HEADLINE)
nib.Text("Subheadline", font=nib.Font.SUBHEADLINE)
nib.Text("Body", font=nib.Font.BODY)
nib.Text("Callout", font=nib.Font.CALLOUT)
nib.Text("Footnote", font=nib.Font.FOOTNOTE)
nib.Text("Caption", font=nib.Font.CAPTION)
nib.Text("Caption 2", font=nib.Font.CAPTION2)
```

| Font | Typical Use |
|------|-------------|
| `Font.LARGE_TITLE` | Screen titles, hero text |
| `Font.TITLE` | Section titles |
| `Font.TITLE2` | Secondary titles |
| `Font.TITLE3` | Tertiary titles |
| `Font.HEADLINE` | Row titles, bold labels |
| `Font.SUBHEADLINE` | Subtitles, secondary labels |
| `Font.BODY` | Main content text (default) |
| `Font.CALLOUT` | Callout boxes, hints |
| `Font.FOOTNOTE` | Footer text, fine print |
| `Font.CAPTION` | Labels below images |
| `Font.CAPTION2` | Smallest caption text |

---

## Custom Size

Use `Font.system()` to create a system font with a specific point size and optional weight:

```python
nib.Text("18pt Regular", font=nib.Font.system(18))
nib.Text("24pt Bold", font=nib.Font.system(24, nib.FontWeight.BOLD))
nib.Text("14pt Light", font=nib.Font.system(14, nib.FontWeight.LIGHT))
```

---

## Font Weight

The `FontWeight` enum provides all standard weights:

| Weight | Constant |
|--------|----------|
| Ultra Light | `nib.FontWeight.ULTRA_LIGHT` |
| Thin | `nib.FontWeight.THIN` |
| Light | `nib.FontWeight.LIGHT` |
| Regular | `nib.FontWeight.REGULAR` |
| Medium | `nib.FontWeight.MEDIUM` |
| Semibold | `nib.FontWeight.SEMIBOLD` |
| Bold | `nib.FontWeight.BOLD` |
| Heavy | `nib.FontWeight.HEAVY` |
| Black | `nib.FontWeight.BLACK` |

You can also apply weight as a standalone modifier using `font_weight`:

```python
nib.Text("Bold Body", font=nib.Font.BODY, font_weight=nib.FontWeight.BOLD)
```

---

## Custom Fonts

Use `Font.custom()` to specify a font family by name. The font must be installed on the system or registered with the app.

```python
nib.Text("Custom Font", font=nib.Font.custom("Inter", size=16))
nib.Text("Weighted", font=nib.Font.custom("Inter", size=16, weight=nib.FontWeight.SEMIBOLD))
```

### Loading Custom Font Files

There are two ways to load custom font files (`.ttf`, `.otf`, `.ttc`):

**1. Auto-detection from the `assets/` directory** (recommended)

Place font files anywhere inside your project's `assets/` folder. Nib scans this directory on startup and registers every `.ttf`, `.otf`, `.ttc`, `.woff`, and `.woff2` file it finds. The font name is derived from the filename without extension.

```
my_project/
  main.py
  assets/
    Inter-Regular.ttf
    Inter-Bold.ttf
    JetBrainsMono-Regular.ttf
```

```python
# Fonts are auto-detected from assets/ -- no registration needed
nib.Text("Hello", font=nib.Font.custom("Inter-Regular", size=16))
nib.Text("Code", font=nib.Font.custom("JetBrainsMono-Regular", size=14))
```

**2. Manual registration via `app.fonts`**

For fonts stored elsewhere, register them by setting `app.fonts` to a dictionary mapping names to absolute file paths or URLs:

```python
def main(app: nib.App):
    app.fonts = {
        "CustomFont": "/Users/me/fonts/CustomFont.ttf",
        "WebFont": "https://example.com/fonts/WebFont.otf",
    }

    app.build(
        nib.Text("Custom", font=nib.Font.custom("CustomFont", size=16))
    )
```

!!! note
    Auto-detected fonts and manually registered fonts are merged. If the same name appears in both, the manual registration takes precedence.

---

## TextStyle

`TextStyle` groups font, decorations, and spacing into a single reusable object. Use it with the `style` parameter on `Text`.

```python
nib.Text("Styled", style=nib.TextStyle(bold=True, italic=True, underline=True))
```

Available `TextStyle` attributes:

| Attribute | Type | Description |
|-----------|------|-------------|
| `font` | `Font` | Font to use |
| `color` | `str` | Text color |
| `weight` | `str` | Font weight |
| `bold` | `bool` | Bold text |
| `italic` | `bool` | Italic text |
| `strikethrough` | `bool` | Strikethrough line |
| `strikethrough_color` | `str` | Color of strikethrough |
| `underline` | `bool` | Underline text |
| `underline_color` | `str` | Color of underline |
| `monospaced` | `bool` | Monospaced font |
| `monospaced_digit` | `bool` | Monospaced digits (for aligned numbers) |
| `kerning` | `float` | Letter spacing |
| `tracking` | `float` | Uniform spacing between characters |
| `baseline_offset` | `float` | Vertical offset from baseline |

### Combining decorations

```python
# Bold, italic, and underlined
nib.Text(
    "Fancy Text",
    style=nib.TextStyle(
        font=nib.Font.system(18),
        bold=True,
        italic=True,
        underline=True,
        underline_color="blue",
        kerning=1.5,
    ),
)
```

### Monospaced digits

Use `monospaced_digit` for numbers that need to align vertically (clocks, counters, tables):

```python
nib.Text("12:34:56", style=nib.TextStyle(monospaced_digit=True, font=nib.Font.TITLE))
```

### Predefined text styles

`TextStyle` also has predefined presets that mirror the system font hierarchy:

```python
nib.Text("Title", style=nib.TextStyle.TITLE)
nib.Text("Headline", style=nib.TextStyle.HEADLINE)
nib.Text("Body", style=nib.TextStyle.BODY)
nib.Text("Caption", style=nib.TextStyle.CAPTION)
```

---

## AttributedString -- Rich Text

`AttributedString` lets you combine multiple styles within a single `Text` view. Pass a list of attributed strings to the `strings` parameter:

```python
nib.Text(
    strings=[
        nib.AttributedString("Bold", style=nib.TextStyle(bold=True)),
        nib.AttributedString(" Normal "),
        nib.AttributedString("Red", color="red"),
        nib.AttributedString(" Italic", style=nib.TextStyle(italic=True)),
    ],
)
```

Each `AttributedString` accepts:

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | The text segment |
| `style` | `TextStyle` | Full style configuration |
| `color` | `str` or `Color` | Color override |
| `font` | `Font` | Font override |

### Mixing fonts and colors

```python
nib.Text(
    strings=[
        nib.AttributedString(
            "Important: ",
            style=nib.TextStyle(bold=True, color="red"),
        ),
        nib.AttributedString(
            "This is normal body text that follows the warning.",
            font=nib.Font.BODY,
        ),
    ],
)
```

### Status line example

```python
nib.Text(
    strings=[
        nib.AttributedString("Status: ", style=nib.TextStyle(bold=True)),
        nib.AttributedString("Connected", color="green"),
        nib.AttributedString(" | "),
        nib.AttributedString("3 devices", style=nib.TextStyle(monospaced_digit=True)),
    ],
)
```

---

## Full Example

A complete app showcasing typography features:

```python
import nib

def main(app: nib.App):
    app.title = "Typography"
    app.icon = nib.SFSymbol("textformat")
    app.width = 320
    app.height = 500

    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        # System font scale
                        nib.Text("System Fonts", font=nib.Font.HEADLINE),
                        nib.Text("Large Title", font=nib.Font.LARGE_TITLE),
                        nib.Text("Title", font=nib.Font.TITLE),
                        nib.Text("Headline", font=nib.Font.HEADLINE),
                        nib.Text("Body (default)", font=nib.Font.BODY),
                        nib.Text("Caption", font=nib.Font.CAPTION),

                        nib.Divider(),

                        # Weights
                        nib.Text("Font Weights", font=nib.Font.HEADLINE),
                        nib.Text("Ultra Light", font=nib.Font.system(16, nib.FontWeight.ULTRA_LIGHT)),
                        nib.Text("Light", font=nib.Font.system(16, nib.FontWeight.LIGHT)),
                        nib.Text("Regular", font=nib.Font.system(16, nib.FontWeight.REGULAR)),
                        nib.Text("Medium", font=nib.Font.system(16, nib.FontWeight.MEDIUM)),
                        nib.Text("Bold", font=nib.Font.system(16, nib.FontWeight.BOLD)),
                        nib.Text("Black", font=nib.Font.system(16, nib.FontWeight.BLACK)),

                        nib.Divider(),

                        # Text decorations
                        nib.Text("Text Styles", font=nib.Font.HEADLINE),
                        nib.Text("Bold", style=nib.TextStyle(bold=True)),
                        nib.Text("Italic", style=nib.TextStyle(italic=True)),
                        nib.Text("Underline", style=nib.TextStyle(underline=True)),
                        nib.Text("Strikethrough", style=nib.TextStyle(strikethrough=True)),
                        nib.Text("Monospaced", style=nib.TextStyle(monospaced=True)),

                        nib.Divider(),

                        # Attributed string
                        nib.Text("Rich Text", font=nib.Font.HEADLINE),
                        nib.Text(
                            strings=[
                                nib.AttributedString("Hello ", color="blue"),
                                nib.AttributedString("World", style=nib.TextStyle(bold=True, color="red")),
                                nib.AttributedString("!", font=nib.Font.TITLE),
                            ],
                        ),
                    ],
                    spacing=6,
                    alignment=nib.HorizontalAlignment.LEADING,
                    padding=16,
                ),
            ],
        )
    )

nib.run(main)
```
