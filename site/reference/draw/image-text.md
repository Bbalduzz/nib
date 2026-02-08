# Image & Text Drawing

Commands for drawing images and text on a [Canvas](../views/effects/canvas.md). These complement the shape primitives by allowing raster content and typographic elements on the drawing surface.

---

## Text

Draws a text string at a specified position on the canvas. Supports font configuration, color, alignment, and text styles.

### Constructor

```python
nib.draw.Text(content, x, y, font=None, fill="#000000", alignment="left",
              opacity=1.0, style=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `str` | *required* | The text string to draw. |
| `x` | `float` | *required* | X coordinate of the text origin. |
| `y` | `float` | *required* | Y coordinate of the text origin. |
| `font` | `Font` | `None` | Font configuration (`nib.Font` instance). Uses system default when `None`. |
| `fill` | `str \| Color` | `"#000000"` | Text color. Accepts hex strings or `nib.Color` objects. |
| `alignment` | `HorizontalAlignment \| str` | `"left"` | Text alignment: `"left"`, `"center"`, or `"right"`. Also accepts `nib.HorizontalAlignment` enum values. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |
| `style` | `TextStyle` | `None` | Optional `nib.TextStyle` for additional styling (bold, italic, etc.). |

### Examples

#### Simple text

```python
import nib

canvas = nib.Canvas(width=400, height=200, background_color="#1e1e1e")
canvas.draw([
    nib.draw.Text("Hello, Canvas!", x=20, y=50, fill="#ffffff"),
])
```

#### Styled text with font and color

```python
import nib

canvas = nib.Canvas(width=400, height=200)
canvas.draw([
    nib.draw.Text(
        "Bold Title",
        x=200,
        y=50,
        font=nib.Font.system(24, weight=nib.FontWeight.BOLD),
        fill=nib.Color.RED,
        alignment=nib.HorizontalAlignment.CENTER,
    ),
    nib.draw.Text(
        "Subtitle text",
        x=200,
        y=90,
        font=nib.Font.system(14),
        fill="#888888",
        alignment="center",
    ),
])
```

#### Multiple text elements

```python
import nib

canvas = nib.Canvas(width=400, height=300, background_color="#f5f5f5")
canvas.draw([
    nib.draw.Text("Left aligned", x=20, y=40, fill="#333333"),
    nib.draw.Text("Center aligned", x=200, y=80, fill="#333333", alignment="center"),
    nib.draw.Text("Right aligned", x=380, y=120, fill="#333333", alignment="right"),
])
```

---

## Image

Draws a raster image on the canvas from raw JPEG/PNG bytes. Images can be scaled to a specific width and height, or drawn at their original resolution.

### Constructor

```python
nib.draw.Image(data, x=0, y=0, width=None, height=None, opacity=1.0)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | `bytes` | *required* | Raw image bytes (JPEG, PNG, or other formats supported by macOS). |
| `x` | `float` | `0` | X coordinate of the top-left corner. |
| `y` | `float` | `0` | Y coordinate of the top-left corner. |
| `width` | `float` | `None` | Width to draw the image. `None` uses the original image width. |
| `height` | `float` | `None` | Height to draw the image. `None` uses the original image height. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

### Examples

#### Drawing from file

```python
import nib

canvas = nib.Canvas(width=400, height=300)

with open("photo.jpg", "rb") as f:
    canvas.draw([
        nib.draw.Image(data=f.read(), x=0, y=0),
    ])
```

#### Scaled image

```python
import nib

canvas = nib.Canvas(width=400, height=300)

with open("icon.png", "rb") as f:
    canvas.draw([
        nib.draw.Image(data=f.read(), x=10, y=10, width=200, height=150),
    ])
```

#### Semi-transparent overlay

```python
import nib

canvas = nib.Canvas(width=400, height=300)

with open("background.jpg", "rb") as bg, open("overlay.png", "rb") as fg:
    canvas.draw([
        nib.draw.Image(data=bg.read(), x=0, y=0, width=400, height=300),
        nib.draw.Image(data=fg.read(), x=50, y=50, width=100, height=100, opacity=0.6),
    ])
```

#### Using PIL/Pillow

```python
import nib
import io
from PIL import Image as PILImage

canvas = nib.Canvas(width=400, height=300)

img = PILImage.open("photo.jpg")
img = img.resize((200, 150))
buffer = io.BytesIO()
img.save(buffer, format="JPEG")

canvas.draw([
    nib.draw.Image(data=buffer.getvalue(), x=100, y=75),
])
```
