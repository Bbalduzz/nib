# Draw Module

The `nib.draw` module provides declarative drawing commands for the [Canvas](../views/effects/canvas.md) view. Commands describe shapes, images, text, and paths that are rendered via Core Graphics on macOS with GPU acceleration.

All drawing is performed through command objects that are passed to `canvas.draw()`, `canvas.append()`, or provided as the `commands` parameter on the Canvas constructor. Commands are dataclasses and can be freely created, stored, and reused.

## Sections

| Section | Description |
|---------|-------------|
| [Primitives](primitives.md) | Shape commands: `Rect`, `Circle`, `Ellipse`, `Line`, `Arc`, `Path`, `Polygon`, `BezierPath`, `Points`, `Shadow`, `Fill`, `ColorFill`. |
| [Paint & Gradients](paint.md) | `Paint` styling class, `PaintStyle`, `StrokeCap`, `StrokeJoin` enums, and gradient fills: `LinearGradient`, `RadialGradient`, `SweepGradient`. |
| [Path Elements](path-elements.md) | Typed path elements for `BezierPath`: `MoveTo`, `LineTo`, `CubicTo`, `QuadraticTo`, `Close`, `ArcTo`, `Oval`, `SubPath`. |
| [Image & Text](image-text.md) | `Image` (raw bytes) and `Text` drawing commands with font and alignment support. |

## Quick example

```python
import nib

def main(app: nib.App):
    canvas = nib.Canvas(width=400, height=300, background_color="#1e1e1e")
    canvas.draw([
        # Rounded rectangle with gradient fill
        nib.draw.Rect(
            x=20, y=20, width=160, height=100,
            fill=nib.draw.LinearGradient(
                start=(20, 20), end=(180, 120),
                colors=["#6366F1", "#EC4899"],
            ),
            corner_radius=12,
        ),
        # Circle with radial gradient
        nib.draw.Circle(
            cx=300, cy=80, radius=50,
            fill=nib.draw.RadialGradient(
                center=(300, 80), radius=50,
                colors=["#FBBF24", "#F97316"],
            ),
        ),
        # Connecting line
        nib.draw.Line(x1=180, y1=70, x2=250, y2=80, stroke="#ffffff", stroke_width=2),
        # Label
        nib.draw.Text("Dashboard", x=20, y=260, fill="#ffffff"),
    ])

    app.build(canvas)

nib.run(main)
```

## Color values

All color parameters in draw commands accept either:

- **Hex strings**: `"#FF0000"`, `"#ff0000"`, `"FF0000"`
- **nib.Color objects**: `nib.Color.RED`, `nib.Color(hex="#FF0000")`

Gradient fills (`LinearGradient`, `RadialGradient`, `SweepGradient`) can be used in place of solid colors on any `fill` parameter.
