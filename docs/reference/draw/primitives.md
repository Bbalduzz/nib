# Drawing Primitives

Shape and utility commands for drawing on a [Canvas](../views/effects/canvas.md). All primitives are dataclasses inheriting from `DrawCommand` and are passed to `canvas.draw()` or `canvas.append()`.

Color parameters accept hex strings (`"#FF0000"`) or `nib.Color` objects. Fill parameters additionally accept gradient objects (`LinearGradient`, `RadialGradient`, `SweepGradient`).

---

## Rect

A rectangle drawing command.

```python
nib.draw.Rect(x, y, width, height, corner_radius=0, fill=None, stroke=None,
              stroke_width=1, opacity=1.0, blend_mode=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | *required* | X coordinate of the top-left corner. |
| `y` | `float` | *required* | Y coordinate of the top-left corner. |
| `width` | `float` | *required* | Width of the rectangle. |
| `height` | `float` | *required* | Height of the rectangle. |
| `corner_radius` | `float` | `0` | Radius for rounded corners. `0` for sharp corners. |
| `fill` | `str \| Color \| Gradient` | `None` | Fill color or gradient. |
| `stroke` | `str \| Color` | `None` | Stroke (outline) color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |
| `blend_mode` | `BlendMode` | `None` | Blend mode for compositing. |

```python
nib.draw.Rect(x=10, y=10, width=100, height=60, fill="#3498db", corner_radius=8)
```

---

## Circle

A circle drawing command.

```python
nib.draw.Circle(cx, cy, radius, fill=None, stroke=None, stroke_width=1,
                opacity=1.0, blend_mode=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cx` | `float` | *required* | X coordinate of the center. |
| `cy` | `float` | *required* | Y coordinate of the center. |
| `radius` | `float` | *required* | Radius of the circle. |
| `fill` | `str \| Color \| Gradient` | `None` | Fill color or gradient. |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |
| `blend_mode` | `BlendMode` | `None` | Blend mode for compositing. |

```python
nib.draw.Circle(cx=100, cy=100, radius=40, fill="#e74c3c")
```

---

## Ellipse

An ellipse drawing command.

```python
nib.draw.Ellipse(cx, cy, rx, ry, fill=None, stroke=None, stroke_width=1,
                 opacity=1.0, blend_mode=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cx` | `float` | *required* | X coordinate of the center. |
| `cy` | `float` | *required* | Y coordinate of the center. |
| `rx` | `float` | *required* | Horizontal radius. |
| `ry` | `float` | *required* | Vertical radius. |
| `fill` | `str \| Color \| Gradient` | `None` | Fill color or gradient. |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |
| `blend_mode` | `BlendMode` | `None` | Blend mode for compositing. |

```python
nib.draw.Ellipse(cx=150, cy=100, rx=80, ry=40, fill="#2ecc71", stroke="#27ae60")
```

---

## Line

A straight line drawing command.

```python
nib.draw.Line(x1, y1, x2, y2, stroke="#000000", stroke_width=1,
              line_cap="butt", opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x1` | `float` | *required* | X coordinate of the start point. |
| `y1` | `float` | *required* | Y coordinate of the start point. |
| `x2` | `float` | *required* | X coordinate of the end point. |
| `y2` | `float` | *required* | Y coordinate of the end point. |
| `stroke` | `str \| Color` | `"#000000"` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `line_cap` | `str` | `"butt"` | Line cap style: `"butt"`, `"round"`, or `"square"`. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
nib.draw.Line(x1=10, y1=200, x2=390, y2=200, stroke="#2ecc71", stroke_width=2)
```

---

## Arc

An arc drawing command.

```python
nib.draw.Arc(cx, cy, radius, start_angle, end_angle, clockwise=True,
             fill=None, stroke=None, stroke_width=1, opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cx` | `float` | *required* | X coordinate of the center. |
| `cy` | `float` | *required* | Y coordinate of the center. |
| `radius` | `float` | *required* | Radius of the arc. |
| `start_angle` | `float` | *required* | Start angle in radians. |
| `end_angle` | `float` | *required* | End angle in radians. |
| `clockwise` | `bool` | `True` | Whether to draw in the clockwise direction. |
| `fill` | `str \| Color` | `None` | Fill color for the arc wedge. |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
import math

nib.draw.Arc(cx=100, cy=100, radius=50, start_angle=0, end_angle=math.pi,
             stroke="#9b59b6", stroke_width=3)
```

---

## Path

A polyline/polygon from a list of coordinate points.

```python
nib.draw.Path(points, closed=False, fill=None, stroke=None, stroke_width=1,
              line_join="miter", opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `points` | `list[tuple[float, float]]` | *required* | List of `(x, y)` coordinate tuples. |
| `closed` | `bool` | `False` | Whether to close the path back to the first point. |
| `fill` | `str \| Color` | `None` | Fill color (only meaningful when `closed=True`). |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `line_join` | `str` | `"miter"` | Line join style: `"miter"`, `"round"`, or `"bevel"`. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
nib.draw.Path(
    points=[(10, 10), (100, 50), (50, 120)],
    closed=True,
    fill="#3498db",
    stroke="#2980b9",
)
```

---

## Polygon

A closed polygon. Convenience wrapper around `Path` with `closed=True`.

```python
nib.draw.Polygon(points, fill=None, stroke=None, stroke_width=1, opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `points` | `list[tuple[float, float]]` | *required* | List of `(x, y)` coordinate tuples defining the polygon vertices. |
| `fill` | `str \| Color` | `None` | Fill color. |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
nib.draw.Polygon(
    points=[(50, 0), (100, 100), (0, 100)],
    fill="#e74c3c",
)
```

---

## BezierPath

A bezier path built from typed path elements or legacy dict commands. Use the typed elements API (recommended) for type safety and IDE support. See [Path Elements](path-elements.md) for the full list of element types.

```python
nib.draw.BezierPath(elements=None, commands=None, fill=None, stroke=None,
                    stroke_width=1, opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `elements` | `list[PathElement]` | `None` | List of typed path elements (`MoveTo`, `LineTo`, `CubicTo`, etc.). Recommended. |
| `commands` | `list[dict]` | `None` | Legacy dict format. Deprecated; use `elements` instead. |
| `fill` | `str \| Color \| Gradient` | `None` | Fill color or gradient. |
| `stroke` | `str \| Color` | `None` | Stroke color. |
| `stroke_width` | `float` | `1` | Width of the stroke. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
from nib.draw import BezierPath, MoveTo, CubicTo, Close

nib.draw.BezierPath(
    elements=[
        MoveTo(100, 50),
        CubicTo(cp1x=100, cp1y=0, cp2x=50, cp2y=0, x=50, y=50),
        CubicTo(cp1x=50, cp1y=80, cp2x=100, cp2y=120, x=100, y=150),
        Close(),
    ],
    fill="#FF0000",
)
```

---

## Points

Draws multiple points, lines between pairs, or a connected polygon.

```python
nib.draw.Points(points, point_mode=PointMode.POINTS, stroke="#000000",
                stroke_width=2, stroke_cap="round", opacity=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `points` | `list[tuple[float, float]]` | *required* | List of `(x, y)` coordinate tuples. |
| `point_mode` | `PointMode` | `PointMode.POINTS` | How to interpret points: `POINTS` (individual dots), `LINES` (pairs of points as line segments), `POLYGON` (connected segments). |
| `stroke` | `str \| Color` | `"#000000"` | Stroke/point color. |
| `stroke_width` | `float` | `2` | Point size or line width. |
| `stroke_cap` | `str` | `"round"` | Cap style for points/lines. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |

```python
nib.draw.Points(
    points=[(10, 10), (50, 50), (100, 30)],
    point_mode=nib.draw.PointMode.POINTS,
    stroke=nib.Color.RED,
    stroke_width=5,
)
```

---

## Shadow

Draws a material-elevation shadow under a shape defined by a point path.

```python
nib.draw.Shadow(path, elevation=5, color="#000000", opacity=0.3)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `list[tuple[float, float]]` | *required* | List of `(x, y)` points defining the shadow shape. |
| `elevation` | `float` | `5` | Shadow elevation (material design style). |
| `color` | `str \| Color` | `"#000000"` | Shadow color. |
| `opacity` | `float` | `0.3` | Shadow opacity. |

```python
nib.draw.Shadow(
    path=[(10, 10), (110, 10), (110, 110), (10, 110)],
    elevation=10,
    color="#000000",
)
```

---

## Fill

Fills the entire canvas with a solid color or gradient.

```python
nib.draw.Fill(fill="#FFFFFF", blend_mode=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fill` | `str \| Color \| Gradient` | `"#FFFFFF"` | Fill color or gradient. |
| `blend_mode` | `BlendMode` | `None` | Blend mode for compositing. |

```python
nib.draw.Fill(fill=nib.draw.LinearGradient(
    start=(0, 0), end=(400, 300),
    colors=[nib.Color.RED, nib.Color.BLUE],
))
```

---

## ColorFill

Fills the canvas with a color using a specific blend mode. Useful for tinting effects.

```python
nib.draw.ColorFill(color="#000000", blend_mode=BlendMode.NORMAL)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `color` | `str \| Color` | `"#000000"` | Color to paint. |
| `blend_mode` | `BlendMode` | `BlendMode.NORMAL` | Blend mode to apply. |

```python
nib.draw.ColorFill(color=nib.Color.RED, blend_mode=nib.BlendMode.MULTIPLY)
```
