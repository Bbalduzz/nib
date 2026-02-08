# Image Enums

Nib provides several enums that control how images, SF Symbols, and text content are displayed.

---

## ImageRenderingMode

Controls how an `Image` view renders its content.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ImageRenderingMode.ORIGINAL` | `.original` | Render the image with its original colors. |
| `ImageRenderingMode.TEMPLATE` | `.template` | Render the image as a template, using the foreground color. |

```python
import nib

# Original colors preserved
nib.Image(source="photo.png", rendering_mode=nib.ImageRenderingMode.ORIGINAL)

# Tinted with foreground color
nib.Image(
    source="icon.png",
    rendering_mode=nib.ImageRenderingMode.TEMPLATE,
    foreground_color=nib.Color.BLUE,
)
```

---

## SymbolScale

Controls the scale of SF Symbols relative to surrounding text.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `SymbolScale.SMALL` | `.small` | Smaller than surrounding text. |
| `SymbolScale.MEDIUM` | `.medium` | Matches surrounding text size (default). |
| `SymbolScale.LARGE` | `.large` | Larger than surrounding text. |

```python
import nib

nib.Image(
    system_name="star.fill",
    symbol_scale=nib.SymbolScale.LARGE,
    foreground_color=nib.Color.YELLOW,
)
```

---

## SymbolRenderingMode

Controls how SF Symbols render their colors.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `SymbolRenderingMode.MONOCHROME` | `.monochrome` | Single color using the foreground color. |
| `SymbolRenderingMode.HIERARCHICAL` | `.hierarchical` | Multiple layers with varying opacity of the foreground color. |
| `SymbolRenderingMode.PALETTE` | `.palette` | Custom colors for each layer. |
| `SymbolRenderingMode.MULTICOLOR` | `.multicolor` | System-defined multicolor rendering. |

```python
import nib

# Hierarchical rendering (depth through opacity)
nib.Image(
    system_name="cloud.sun.rain.fill",
    symbol_rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
    foreground_color=nib.Color.BLUE,
)

# Multicolor rendering (system colors)
nib.Image(
    system_name="cloud.sun.rain.fill",
    symbol_rendering_mode=nib.SymbolRenderingMode.MULTICOLOR,
)
```

---

## ContentMode

Controls how an image is scaled to fit its frame. Used with the `content_mode` parameter on `Image` views.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ContentMode.FIT` | `.fit` | Scale to fit within bounds while maintaining aspect ratio. The entire image is visible. |
| `ContentMode.FILL` | `.fill` | Scale to fill bounds while maintaining aspect ratio. Parts of the image may be clipped. |

```python
import nib

# Fit within frame (may have empty space)
nib.Image(source="photo.png", content_mode=nib.ContentMode.FIT, width=200, height=150)

# Fill frame (may clip edges)
nib.Image(
    source="photo.png",
    content_mode=nib.ContentMode.FILL,
    width=200,
    height=150,
    clip_shape="circle",
)
```

---

## TruncationMode

Controls where text is truncated when it exceeds the available space.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `TruncationMode.HEAD` | `.head` | Truncate at the beginning: `"...end of text"`. |
| `TruncationMode.MIDDLE` | `.middle` | Truncate in the middle: `"start...end"`. |
| `TruncationMode.TAIL` | `.tail` | Truncate at the end: `"start of text..."` (default). |

```python
import nib

nib.Text(
    "This is a very long text that will be truncated",
    truncation_mode=nib.TruncationMode.MIDDLE,
    line_limit=1,
)
```

---

## TextCase

Transforms the case of displayed text without modifying the underlying value.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `TextCase.UPPERCASE` | `.uppercase` | Display text in all uppercase letters. |
| `TextCase.LOWERCASE` | `.lowercase` | Display text in all lowercase letters. |

```python
import nib

nib.Text("section header", text_case=nib.TextCase.UPPERCASE)
# Displays: "SECTION HEADER"
```

## Examples

### Avatar image with circular clipping

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Image(
                    source="avatar.jpg",
                    content_mode=nib.ContentMode.FILL,
                    width=80,
                    height=80,
                    clip_shape="circle",
                ),
                nib.Text("Jane Doe", font=nib.Font.HEADLINE),
                nib.Text("Online", font=nib.Font.CAPTION, foreground_color=nib.Color.GREEN),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### SF Symbol with different rendering modes

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Image(
                    system_name="heart.fill",
                    symbol_rendering_mode=nib.SymbolRenderingMode.MONOCHROME,
                    foreground_color=nib.Color.RED,
                    symbol_scale=nib.SymbolScale.LARGE,
                ),
                nib.Image(
                    system_name="heart.fill",
                    symbol_rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL,
                    foreground_color=nib.Color.PINK,
                    symbol_scale=nib.SymbolScale.LARGE,
                ),
                nib.Image(
                    system_name="heart.fill",
                    symbol_rendering_mode=nib.SymbolRenderingMode.MULTICOLOR,
                    symbol_scale=nib.SymbolScale.LARGE,
                ),
            ],
            spacing=20,
            padding=16,
        )
    )

nib.run(main)
```
