# Appearance Modifiers

Appearance modifiers control the visual presentation of views, including colors, fills, strokes, opacity, corner rounding, clipping, and visibility.

```python
import nib

nib.Rectangle(
    fill=nib.Color.BLUE,
    stroke="#FF0000",
    stroke_width=2,
    opacity=0.9,
    corner_radius=12,
)
```

---

## foreground_color

Sets the color of text, icons, and other foreground content within a view.

| Type | Default |
|------|---------|
| `Color \| str` | `None` |

Accepts a `Color` object, a named color string, or a hex string.

```python
nib.Text("Blue text", foreground_color=nib.Color.BLUE)
nib.Text("Red text", foreground_color="red")
nib.Text("Custom color", foreground_color="#FF5733")
```

---

## background

Sets a background color or view behind the content. Accepts three types of values:

| Type | Default |
|------|---------|
| `Color \| str \| View` | `None` |

**Color string or Color object:**

```python
nib.Text("On dark bg", background="#1E1E1E", foreground_color="white")
nib.Text("On blue bg", background=nib.Color.BLUE)
```

**Background view** (e.g., a shape with styling):

```python
nib.VStack(
    controls=[nib.Text("Card content")],
    background=nib.Rectangle(
        corner_radius=12,
        fill="#262626",
        stroke="#383837",
        stroke_width=1,
    ),
    padding=16,
)
```

---

## fill

Sets the interior color of shape views (`Rectangle`, `Circle`, `Capsule`, `Ellipse`). Also accepts gradient views.

| Type | Default |
|------|---------|
| `Color \| str` | `None` |

```python
nib.Circle(fill=nib.Color.RED, width=80, height=80)
nib.Rectangle(fill="#333333", width=200, height=100)
```

---

## stroke

Sets the outline color of shape views. Used in combination with `stroke_width`.

| Type | Default |
|------|---------|
| `Color \| str` | `None` |

```python
nib.Circle(stroke=nib.Color.BLUE, stroke_width=2, width=80, height=80)
```

---

## stroke_width

Sets the thickness of the shape outline in points. Only applies when `stroke` is also set.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.Rectangle(stroke="red", stroke_width=3, width=100, height=50)
```

---

## opacity

Controls the transparency of a view and all its children. Values range from `0.0` (fully transparent) to `1.0` (fully opaque).

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.Text("Faded", opacity=0.5)
nib.Rectangle(fill="blue", width=100, height=100, opacity=0.3)
```

Opacity can be updated reactively:

```python
box = nib.Rectangle(fill="blue", width=100, height=100, animation=nib.Animation.easeInOut())

def toggle_opacity():
    box.opacity = 0.2 if (box.opacity or 1.0) > 0.5 else 1.0
```

---

## corner_radius

Rounds the corners of a view's bounds. Accepts a uniform radius or a `CornerRadius` object for per-corner control.

| Type | Default |
|------|---------|
| `float \| CornerRadius` | `None` |

```python
# Uniform corners
nib.Rectangle(fill="blue", corner_radius=10, width=100, height=60)

# Per-corner control
nib.Rectangle(
    fill="blue",
    corner_radius=nib.CornerRadius.vertical(top=16, bottom=0),
    width=100,
    height=60,
)
```

---

## clip_shape

Clips the view's content to a specified shape. Content outside the shape is hidden.

| Type | Default |
|------|---------|
| `str \| View` | `None` |

**String values:** `"circle"`, `"capsule"`, `"rectangle"`

```python
# Circular avatar
nib.Image(source="photo.jpg", width=80, height=80, clip_shape="circle")

# Pill-shaped button
nib.Text("Tag", padding={"horizontal": 12, "vertical": 6}, background="blue", clip_shape="capsule")
```

**Shape view** (for custom corner radius):

```python
nib.Image(
    source="photo.jpg",
    width=200,
    height=150,
    clip_shape=nib.Rectangle(corner_radius=16),
)
```

---

## visible

Controls whether a view is included in the layout tree. When set to `False`, the view is completely removed and does not occupy any layout space. This is different from `opacity=0`, where the view is invisible but still takes up space.

| Type | Default |
|------|---------|
| `bool` | `True` |

```python
label = nib.Text("Conditional content", visible=False)

def show():
    label.visible = True
```

## Examples

### Styled card component

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Card Title", font=nib.Font.HEADLINE),
                nib.Text(
                    "This is a card with custom styling.",
                    foreground_color=nib.Color.SECONDARY,
                ),
            ],
            spacing=8,
            padding=16,
            background=nib.Rectangle(
                corner_radius=12,
                fill="#2A2A2A",
                stroke="#3A3A3A",
                stroke_width=1,
            ),
            shadow_color="black",
            shadow_radius=8,
            shadow_y=4,
        )
    )

nib.run(main)
```

### Shape fills and strokes

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Circle(fill=nib.Color.RED, width=60, height=60),
                nib.Circle(
                    stroke=nib.Color.BLUE,
                    stroke_width=3,
                    width=60,
                    height=60,
                ),
                nib.Rectangle(
                    fill="#333",
                    stroke=nib.Color.ORANGE,
                    stroke_width=2,
                    corner_radius=8,
                    width=60,
                    height=60,
                ),
            ],
            spacing=16,
            padding=20,
        )
    )

nib.run(main)
```
