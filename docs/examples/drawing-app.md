# Drawing App

A freehand drawing application using the Canvas view with pan gesture handling. Demonstrates how to draw lines on a canvas, change stroke color and width, and clear the drawing.

## Full Source

```python
import nib

def main(app: nib.App):
    app.title = "Draw"
    app.icon = nib.SFSymbol("pencil.tip")
    app.width = 440
    app.height = 380

    # Canvas with gesture support
    canvas = nib.Canvas(
        width=420,
        height=300,
        background_color="#FFFFFF",
        enable_gestures=True,
    )

    # Drawing state
    last_x = 0.0
    last_y = 0.0
    stroke_color = "#000000"
    stroke_width = 3

    def on_pan_start(e: nib.PanEvent):
        nonlocal last_x, last_y
        last_x = e.x
        last_y = e.y

    def on_pan_update(e: nib.PanEvent):
        nonlocal last_x, last_y
        canvas.append(
            nib.draw.Line(
                x1=last_x,
                y1=last_y,
                x2=e.x,
                y2=e.y,
                stroke=stroke_color,
                stroke_width=stroke_width,
                line_cap="round",
            )
        )
        last_x = e.x
        last_y = e.y

    canvas.on_pan_start = on_pan_start
    canvas.on_pan_update = on_pan_update

    # Clear canvas
    def clear_canvas():
        canvas.clear()

    # Color selectors
    def set_black():
        nonlocal stroke_color
        stroke_color = "#000000"

    def set_red():
        nonlocal stroke_color
        stroke_color = "#e74c3c"

    def set_blue():
        nonlocal stroke_color
        stroke_color = "#3498db"

    def set_green():
        nonlocal stroke_color
        stroke_color = "#2ecc71"

    # Width selectors
    def set_thin():
        nonlocal stroke_width
        stroke_width = 2

    def set_medium():
        nonlocal stroke_width
        stroke_width = 5

    def set_thick():
        nonlocal stroke_width
        stroke_width = 10

    app.build(
        nib.VStack(
            controls=[
                # Toolbar
                nib.HStack(
                    controls=[
                        nib.Button("Clear", action=clear_canvas),
                        nib.Spacer(),
                        nib.Text("Color:", font=nib.Font.CAPTION),
                        nib.Button("Black", action=set_black),
                        nib.Button("Red", action=set_red),
                        nib.Button("Blue", action=set_blue),
                        nib.Button("Green", action=set_green),
                        nib.Spacer(),
                        nib.Text("Width:", font=nib.Font.CAPTION),
                        nib.Button("Thin", action=set_thin),
                        nib.Button("Med", action=set_medium),
                        nib.Button("Thick", action=set_thick),
                    ],
                    spacing=4,
                ),
                # Canvas with border
                nib.VStack(
                    controls=[canvas],
                    background=nib.Rectangle(
                        corner_radius=5,
                        stroke="#cccccc",
                        stroke_width=1,
                    ),
                ),
            ],
            spacing=10,
            padding=10,
        )
    )

nib.run(main)
```

## Walkthrough

### Creating a Canvas

```python
canvas = nib.Canvas(
    width=420,
    height=300,
    background_color="#FFFFFF",
    enable_gestures=True,
)
```

The `Canvas` view provides a Core Graphics-backed drawing surface. Key parameters:

| Parameter | Description |
|-----------|-------------|
| `width`, `height` | Canvas dimensions in points |
| `background_color` | Fill color for the canvas background |
| `enable_gestures` | When `True`, the canvas emits pan (drag) events |

### Gesture handling

```python
def on_pan_start(e: nib.PanEvent):
    nonlocal last_x, last_y
    last_x = e.x
    last_y = e.y

def on_pan_update(e: nib.PanEvent):
    nonlocal last_x, last_y
    canvas.append(
        nib.draw.Line(
            x1=last_x, y1=last_y,
            x2=e.x, y2=e.y,
            stroke=stroke_color,
            stroke_width=stroke_width,
            line_cap="round",
        )
    )
    last_x = e.x
    last_y = e.y

canvas.on_pan_start = on_pan_start
canvas.on_pan_update = on_pan_update
```

The canvas fires gesture callbacks:

- `on_pan_start` -- Called when the user begins a drag. Records the starting position.
- `on_pan_update` -- Called continuously as the user drags. Draws a line segment from the previous position to the current position.

The `PanEvent` object provides `x` and `y` coordinates relative to the canvas origin.

### Drawing commands

```python
canvas.append(
    nib.draw.Line(
        x1=last_x, y1=last_y,
        x2=e.x, y2=e.y,
        stroke=stroke_color,
        stroke_width=stroke_width,
        line_cap="round",
    )
)
```

The `nib.draw` module provides drawing primitives that can be appended to a canvas:

- `nib.draw.Line` -- A line segment between two points
- `nib.draw.Rect` -- A rectangle
- `nib.draw.Circle` -- A circle
- `nib.draw.Path` -- A custom path with arcs, curves, and lines
- `nib.draw.Text` -- Text rendered at a position

`canvas.append()` adds a drawing command incrementally. The Swift runtime renders it immediately without redrawing existing commands.

`canvas.clear()` removes all drawing commands and resets the canvas.

### Using `line_cap="round"`

The `line_cap` parameter controls how line endpoints are drawn:

- `"round"` -- Rounded endpoints (smooth freehand look)
- `"square"` -- Square endpoints extending beyond the endpoint
- `"butt"` -- Flat endpoints exactly at the endpoint (default)

For freehand drawing, `"round"` produces smooth joins between consecutive line segments.

### Toolbar layout

The toolbar is an `HStack` with buttons and `Spacer` views:

```python
nib.HStack(
    controls=[
        nib.Button("Clear", action=clear_canvas),
        nib.Spacer(),
        nib.Text("Color:", font=nib.Font.CAPTION),
        nib.Button("Black", action=set_black),
        ...
        nib.Spacer(),
        nib.Text("Width:", font=nib.Font.CAPTION),
        nib.Button("Thin", action=set_thin),
        ...
    ],
    spacing=4,
)
```

`Spacer` pushes adjacent views apart, distributing the toolbar into three groups: the clear button on the left, color buttons in the middle, and width buttons on the right.

### Drawing state

```python
stroke_color = "#000000"
stroke_width = 3
```

Drawing settings are stored as plain Python variables. The color and width selector buttons update these variables via `nonlocal`. The next stroke drawn will use the new values. Previously drawn lines are not affected.

### Canvas border

```python
nib.VStack(
    controls=[canvas],
    background=nib.Rectangle(
        corner_radius=5,
        stroke="#cccccc",
        stroke_width=1,
    ),
)
```

The canvas is wrapped in a `VStack` with a `Rectangle` background that provides a subtle border. The `stroke` parameter draws an outline, while `corner_radius` rounds the corners.

### Running

```bash
nib run drawing_app.py
```
