# Canvas Drawing

The Canvas view provides a drawing surface backed by Core Graphics. You can render shapes, lines, text, and images using declarative drawing commands from the `nib.draw` module.

## Creating a canvas

```python
import nib

canvas = nib.Canvas(width=400, height=300, background_color="#1a1a1a")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `float` | `100` | Width of the drawing area in points |
| `height` | `float` | `100` | Height of the drawing area in points |
| `background_color` | `str` | `None` | Background color as hex string, or `None` for transparent |
| `enable_gestures` | `bool` | `False` | Enable pan/hover gesture tracking |

The canvas also accepts all standard view modifiers (`padding`, `opacity`, `corner_radius`, etc.) as keyword arguments.

## Drawing commands

All drawing commands live in the `nib.draw` module. Pass a list of commands to `canvas.draw()`:

```python
canvas.draw([
    nib.draw.Rect(x=10, y=10, width=100, height=50, fill="#3498db"),
    nib.draw.Circle(cx=200, cy=100, radius=40, fill="#e74c3c"),
    nib.draw.Line(x1=10, y1=200, x2=390, y2=200, stroke="#2ecc71"),
    nib.draw.Text("Hello Canvas!", x=10, y=280, fill="#ffffff"),
])
```

### Rect

Draws a rectangle, optionally with rounded corners:

```python
nib.draw.Rect(
    x=10, y=10,
    width=100, height=80,
    corner_radius=8,
    fill="#3498db",
    stroke="#2980b9",
    stroke_width=2,
    opacity=0.9,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | -- | X coordinate of top-left corner |
| `y` | `float` | -- | Y coordinate of top-left corner |
| `width` | `float` | -- | Width of the rectangle |
| `height` | `float` | -- | Height of the rectangle |
| `corner_radius` | `float` | `0` | Radius for rounded corners |
| `fill` | color/gradient | `None` | Fill color or gradient |
| `stroke` | color | `None` | Stroke color |
| `stroke_width` | `float` | `1` | Stroke width |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0 |
| `blend_mode` | `BlendMode` | `None` | Compositing blend mode |

### Circle

Draws a circle from a center point and radius:

```python
nib.draw.Circle(cx=200, cy=100, radius=40, fill="#e74c3c")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cx` | `float` | -- | X coordinate of center |
| `cy` | `float` | -- | Y coordinate of center |
| `radius` | `float` | -- | Circle radius |
| `fill` | color/gradient | `None` | Fill color or gradient |
| `stroke` | color | `None` | Stroke color |
| `stroke_width` | `float` | `1` | Stroke width |
| `opacity` | `float` | `1.0` | Opacity |

### Ellipse

Draws an ellipse with independent horizontal and vertical radii:

```python
nib.draw.Ellipse(cx=150, cy=100, rx=80, ry=40, fill="#9b59b6")
```

### Line

Draws a straight line between two points:

```python
nib.draw.Line(
    x1=10, y1=10,
    x2=200, y2=200,
    stroke="#000000",
    stroke_width=2,
    line_cap="round",  # "butt", "round", or "square"
)
```

### Text

Draws text at a position:

```python
nib.draw.Text(
    "Hello World",
    x=10, y=50,
    fill="#ffffff",
    font=nib.Font.system(20, weight=nib.FontWeight.BOLD),
    alignment=nib.HorizontalAlignment.CENTER,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `str` | -- | The text string to draw |
| `x` | `float` | -- | X coordinate of text origin |
| `y` | `float` | -- | Y coordinate of text origin |
| `fill` | color | `"#000000"` | Text color |
| `font` | `Font` | `None` | Font configuration |
| `alignment` | `HorizontalAlignment` | `"left"` | Text alignment |
| `opacity` | `float` | `1.0` | Opacity |

### Arc

Draws an arc segment:

```python
import math

nib.draw.Arc(
    cx=100, cy=100,
    radius=50,
    start_angle=0,
    end_angle=math.pi,
    fill="#f39c12",
    stroke="#e67e22",
)
```

### Path

Draws a path from a list of points:

```python
nib.draw.Path(
    points=[(10, 10), (100, 50), (50, 100)],
    closed=True,
    fill="#2ecc71",
    stroke="#27ae60",
    stroke_width=2,
)
```

### Polygon

A convenience wrapper around `Path` with `closed=True`:

```python
nib.draw.Polygon(
    points=[(100, 10), (190, 80), (160, 170), (40, 170), (10, 80)],
    fill="#1abc9c",
)
```

### BezierPath

Draws complex curves using typed path elements:

```python
from nib.draw import BezierPath, MoveTo, CubicTo, QuadraticTo, LineTo, Close

nib.draw.BezierPath(
    elements=[
        MoveTo(50, 150),
        CubicTo(cp1x=50, cp1y=50, cp2x=150, cp2y=50, x=150, y=150),
        Close(),
    ],
    fill="#e74c3c",
    stroke="#c0392b",
)
```

Available path elements:

| Element | Parameters | Description |
|---------|------------|-------------|
| `MoveTo(x, y)` | x, y | Move to a point without drawing |
| `LineTo(x, y)` | x, y | Draw a straight line to a point |
| `CubicTo(...)` | cp1x, cp1y, cp2x, cp2y, x, y | Cubic bezier curve |
| `QuadraticTo(...)` | cp1x, cp1y, x, y, w | Quadratic bezier curve |
| `Close()` | -- | Close the path back to the start |
| `ArcTo(...)` | x, y, radius, rotation, large_arc, clockwise | Arc segment |
| `Oval(...)` | x, y, width, height | Ellipse inscribed in rectangle |
| `PathRect(...)` | x, y, width, height, border_radius | Rectangle sub-path |
| `SubPath(...)` | x, y, elements | Nested sub-path at offset |

### Image

Draws an image from raw bytes:

```python
with open("photo.jpg", "rb") as f:
    nib.draw.Image(
        data=f.read(),
        x=10, y=10,
        width=200,
        height=150,
    )
```

### Points

Draws a set of points with different modes:

```python
nib.draw.Points(
    points=[(10, 10), (50, 50), (100, 30), (150, 80)],
    point_mode=nib.draw.PointMode.POINTS,  # POINTS, LINES, or POLYGON
    stroke="#e74c3c",
    stroke_width=5,
    stroke_cap="round",
)
```

### Fill

Fills the entire canvas with a color or gradient:

```python
nib.draw.Fill(fill="#1a1a1a")
```

## Colors

All color parameters accept hex strings or `nib.Color` objects:

```python
# Hex strings
nib.draw.Rect(x=0, y=0, width=100, height=100, fill="#FF5733")

# nib.Color constants
nib.draw.Circle(cx=50, cy=50, radius=30, fill=nib.Color.RED)
```

## Gradients

Fill parameters on `Rect`, `Circle`, `Ellipse`, `BezierPath`, and `Fill` accept gradient objects instead of solid colors:

### LinearGradient

```python
nib.draw.Rect(
    x=0, y=0, width=200, height=100,
    fill=nib.draw.LinearGradient(
        start=(0, 0),
        end=(200, 100),
        colors=["#FF0000", "#0000FF"],
        stops=[0.0, 1.0],  # optional
    ),
)
```

### RadialGradient

```python
nib.draw.Circle(
    cx=100, cy=100, radius=80,
    fill=nib.draw.RadialGradient(
        center=(100, 100),
        radius=80,
        colors=[nib.Color.YELLOW, nib.Color.RED],
    ),
)
```

### SweepGradient

```python
nib.draw.Circle(
    cx=100, cy=100, radius=80,
    fill=nib.draw.SweepGradient(
        center=(100, 100),
        colors=[nib.Color.RED, nib.Color.GREEN, nib.Color.BLUE, nib.Color.RED],
    ),
)
```

## Drawing methods

The `Canvas` provides three methods to manage drawing commands:

### `canvas.draw(commands)`

Replaces all current commands and triggers a re-render:

```python
canvas.draw([
    nib.draw.Rect(x=0, y=0, width=100, height=100, fill="#3498db"),
])
```

### `canvas.append(command)`

Adds a single command to the existing list:

```python
canvas.append(nib.draw.Circle(cx=50, cy=50, radius=20, fill="#e74c3c"))
```

### `canvas.clear()`

Removes all commands and updates the display:

```python
canvas.clear()
```

## Gesture handling

Enable gestures to respond to mouse and trackpad input on the canvas. Gestures are enabled automatically when you provide any gesture callback:

```python
canvas = nib.Canvas(
    width=400, height=300,
    on_pan_start=handle_start,
    on_pan_update=handle_update,
    on_pan_end=handle_end,
    on_hover=handle_hover,
)
```

You can also set gesture callbacks after creation:

```python
canvas = nib.Canvas(width=400, height=300)
canvas.on_pan_start = handle_start
canvas.on_pan_update = handle_update
```

### PanEvent

All gesture callbacks receive a `PanEvent` dataclass with the cursor coordinates:

```python
from nib import PanEvent

def handle_update(e: PanEvent):
    print(f"x={e.x}, y={e.y}")
```

| Field | Type | Description |
|-------|------|-------------|
| `x` | `float` | X coordinate in canvas coordinates |
| `y` | `float` | Y coordinate in canvas coordinates |

### Available gesture callbacks

| Callback | Fired when |
|----------|-----------|
| `on_pan_start` | Mouse button pressed down on canvas |
| `on_pan_update` | Mouse dragged while button held |
| `on_pan_end` | Mouse button released |
| `on_hover` | Mouse moves over canvas (no button held) |

## Complete example: drawing app

A simple drawing application that lets you draw freehand lines by dragging the mouse:

```python
import nib


def main(app: nib.App):
    app.title = "Draw"
    app.icon = nib.SFSymbol("pencil.tip")
    app.width = 420
    app.height = 380

    canvas = nib.Canvas(
        width=400, height=300,
        background_color="#ffffff",
    )

    color = "#000000"
    stroke_width = 3
    last_pos = None

    def on_start(e: nib.PanEvent):
        nonlocal last_pos
        last_pos = (e.x, e.y)

    def on_update(e: nib.PanEvent):
        nonlocal last_pos
        if last_pos:
            canvas.append(nib.draw.Line(
                x1=last_pos[0], y1=last_pos[1],
                x2=e.x, y2=e.y,
                stroke=color,
                stroke_width=stroke_width,
                line_cap="round",
            ))
            last_pos = (e.x, e.y)

    def on_end(e: nib.PanEvent):
        nonlocal last_pos
        last_pos = None

    canvas.on_pan_start = on_start
    canvas.on_pan_update = on_update
    canvas.on_pan_end = on_end

    def clear_canvas():
        canvas.clear()

    def set_black():
        nonlocal color
        color = "#000000"

    def set_red():
        nonlocal color
        color = "#e74c3c"

    def set_blue():
        nonlocal color
        color = "#3498db"

    app.build(
        nib.VStack(
            controls=[
                canvas,
                nib.HStack(
                    controls=[
                        nib.Button("Black", action=set_black),
                        nib.Button("Red", action=set_red),
                        nib.Button("Blue", action=set_blue),
                        nib.Spacer(),
                        nib.Button("Clear", action=clear_canvas),
                    ],
                    spacing=8,
                ),
            ],
            spacing=8,
            padding=10,
        )
    )


nib.run(main)
```

!!! tip
    Use `canvas.append()` inside `on_pan_update` for efficient incremental drawing. Using `canvas.draw()` with the full command list on every mouse move would be slower for complex drawings.

## Reactive properties

Canvas dimensions and background color are reactive. Changing them triggers a re-render:

```python
canvas.canvas_width = 500
canvas.canvas_height = 400
canvas.background_color = "#2c3e50"
```
