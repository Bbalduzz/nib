# Path Elements

Typed path elements for constructing bezier paths used with `BezierPath`. Each element is a dataclass representing a segment of a path. Elements are composed into a list and passed to the `BezierPath(elements=[...])` parameter.

All path elements inherit from the `PathElement` base class.

---

## MoveTo

Starts a new sub-path at the given point. Does not draw anything; it sets the current point for subsequent drawing elements.

```python
nib.draw.MoveTo(x, y)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `float` | X coordinate of the point. |
| `y` | `float` | Y coordinate of the point. |

---

## LineTo

Draws a straight line from the current point to the given point.

```python
nib.draw.LineTo(x, y)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `float` | X coordinate of the endpoint. |
| `y` | `float` | Y coordinate of the endpoint. |

---

## CubicTo

Draws a cubic bezier curve from the current point to `(x, y)` using two control points. Cubic beziers provide smooth curves with two degrees of curvature control.

```python
nib.draw.CubicTo(cp1x, cp1y, cp2x, cp2y, x, y)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `cp1x` | `float` | First control point X coordinate. |
| `cp1y` | `float` | First control point Y coordinate. |
| `cp2x` | `float` | Second control point X coordinate. |
| `cp2y` | `float` | Second control point Y coordinate. |
| `x` | `float` | Endpoint X coordinate. |
| `y` | `float` | Endpoint Y coordinate. |

---

## QuadraticTo

Draws a quadratic bezier curve from the current point to `(x, y)` using one control point. The optional weight `w` controls the conic section type.

```python
nib.draw.QuadraticTo(cp1x, cp1y, x, y, w=1.0)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cp1x` | `float` | *required* | Control point X coordinate. |
| `cp1y` | `float` | *required* | Control point Y coordinate. |
| `x` | `float` | *required* | Endpoint X coordinate. |
| `y` | `float` | *required* | Endpoint Y coordinate. |
| `w` | `float` | `1.0` | Weight for conic sections. `w > 1`: hyperbola, `w == 1`: parabola (standard quadratic), `w < 1`: ellipse. |

---

## Close

Closes the current sub-path by drawing a straight line from the current point back to the starting point of the sub-path.

```python
nib.draw.Close()
```

No parameters.

---

## ArcTo

Draws an arc from the current point to `(x, y)` with configurable radius, rotation, and sweep direction.

```python
nib.draw.ArcTo(x, y, radius=0, rotation=0, large_arc=False, clockwise=True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | *required* | Endpoint X coordinate. |
| `y` | `float` | *required* | Endpoint Y coordinate. |
| `radius` | `float` | `0` | Radius of the arc. |
| `rotation` | `float` | `0` | Rotation of the arc in degrees. |
| `large_arc` | `bool` | `False` | Whether to use the large arc sweep. |
| `clockwise` | `bool` | `True` | Whether the arc is drawn clockwise. |

---

## PathArc

Adds an arc segment following the edge of an oval. The arc follows the oval bounded by the rectangle at `(x, y)` with the given `width` and `height`.

!!! note
    Imported as `PathArc` to avoid conflict with the top-level `Arc` draw command. Use `from nib.draw import PathArc`.

```python
nib.draw.PathArc(x, y, width, height, start_angle, sweep_angle)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `float` | Top-left X of the bounding rectangle. |
| `y` | `float` | Top-left Y of the bounding rectangle. |
| `width` | `float` | Width of the bounding rectangle. |
| `height` | `float` | Height of the bounding rectangle. |
| `start_angle` | `float` | Starting angle in radians (0 = 3 o'clock position). |
| `sweep_angle` | `float` | Sweep angle in radians from `start_angle`. Positive is clockwise. |

---

## Oval

Adds an ellipse that fills the given bounding rectangle as a sub-path.

```python
nib.draw.Oval(x, y, width, height)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `float` | Top-left X of the bounding rectangle. |
| `y` | `float` | Top-left Y of the bounding rectangle. |
| `width` | `float` | Width of the bounding rectangle. |
| `height` | `float` | Height of the bounding rectangle. |

---

## PathRect

Adds a rectangle as a new sub-path element, optionally with rounded corners.

!!! note
    Imported as `PathRect` to avoid conflict with the top-level `Rect` draw command. Use `from nib.draw import PathRect`.

```python
nib.draw.PathRect(x, y, width, height, border_radius=None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `float` | *required* | Top-left X of the rectangle. |
| `y` | `float` | *required* | Top-left Y of the rectangle. |
| `width` | `float` | *required* | Width of the rectangle. |
| `height` | `float` | *required* | Height of the rectangle. |
| `border_radius` | `float` | `None` | Corner radius for rounded rectangles. |

---

## SubPath

Embeds a group of path elements at a given offset, creating a translated sub-path within the parent path.

```python
nib.draw.SubPath(x, y, elements)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `float` | X offset for the sub-path. |
| `y` | `float` | Y offset for the sub-path. |
| `elements` | `list[PathElement]` | List of path elements in the sub-path. |

---

## Examples

### Heart shape with cubic beziers

```python
import nib
from nib.draw import BezierPath, MoveTo, CubicTo, Close

canvas = nib.Canvas(width=200, height=200)
canvas.draw([
    BezierPath(
        elements=[
            MoveTo(100, 50),
            CubicTo(cp1x=100, cp1y=0, cp2x=50, cp2y=0, x=50, y=50),
            CubicTo(cp1x=50, cp1y=80, cp2x=100, cp2y=120, x=100, y=150),
            CubicTo(cp1x=100, cp1y=120, cp2x=150, cp2y=80, x=150, y=50),
            CubicTo(cp1x=150, cp1y=0, cp2x=100, cp2y=0, x=100, y=50),
            Close(),
        ],
        fill="#FF0000",
    ),
])
```

### Quadratic bezier curve

```python
import nib
from nib.draw import BezierPath, MoveTo, QuadraticTo, Close

canvas = nib.Canvas(width=200, height=200)
canvas.draw([
    BezierPath(
        elements=[
            MoveTo(25, 125),
            QuadraticTo(cp1x=50, cp1y=25, x=135, y=35),
            QuadraticTo(cp1x=75, cp1y=115, x=135, y=215),
            Close(),
        ],
        fill="#F06292",
    ),
])
```

### Custom shape with mixed elements

```python
import nib
from nib.draw import BezierPath, MoveTo, LineTo, ArcTo, Close

canvas = nib.Canvas(width=300, height=200)
canvas.draw([
    BezierPath(
        elements=[
            MoveTo(50, 100),
            LineTo(150, 20),
            ArcTo(x=250, y=100, radius=50, clockwise=True),
            LineTo(150, 180),
            Close(),
        ],
        fill="#6366F1",
        stroke="#4F46E5",
        stroke_width=2,
    ),
])
```
