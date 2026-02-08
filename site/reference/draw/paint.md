# Paint & Gradients

Styling classes for controlling how shapes are drawn on a [Canvas](../views/effects/canvas.md). The `Paint` class acts as a "paintbrush" that determines color, stroke style, gradients, and effects. Gradient classes provide `LinearGradient`, `RadialGradient`, and `SweepGradient` fills.

All color parameters accept hex strings (`"#FF0000"`) or `nib.Color` objects.

---

## Paint

Defines the full drawing style for shapes. Combines color, stroke properties, gradients, blur, and blend mode into a single configuration object.

### Constructor

```python
nib.draw.Paint(
    color=None,
    style=PaintStyle.FILL,
    stroke_width=1.0,
    stroke_cap=StrokeCap.BUTT,
    stroke_join=StrokeJoin.MITER,
    stroke_miter_limit=4.0,
    opacity=1.0,
    blend_mode=None,
    gradient=None,
    blur=None,
    anti_alias=True,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `color` | `str \| Color` | `None` | Base color for the paint. |
| `style` | `PaintStyle` | `PaintStyle.FILL` | Drawing style: `FILL` or `STROKE`. |
| `stroke_width` | `float` | `1.0` | Width of strokes in points. |
| `stroke_cap` | `StrokeCap` | `StrokeCap.BUTT` | Shape at line ends: `BUTT`, `ROUND`, or `SQUARE`. |
| `stroke_join` | `StrokeJoin` | `StrokeJoin.MITER` | Shape at corners: `MITER`, `ROUND`, or `BEVEL`. |
| `stroke_miter_limit` | `float` | `4.0` | Limit for miter joins before they are beveled. |
| `opacity` | `float` | `1.0` | Opacity from 0.0 to 1.0. |
| `blend_mode` | `BlendMode` | `None` | Blend mode for compositing (e.g., `nib.BlendMode.MULTIPLY`). |
| `gradient` | `LinearGradient \| RadialGradient \| SweepGradient` | `None` | Gradient fill. Overrides `color` for fill rendering. |
| `blur` | `Blur` | `None` | Blur effect applied to the paint. |
| `anti_alias` | `bool` | `True` | Whether to apply anti-aliasing. |

### Example

```python
import nib

paint = nib.draw.Paint(
    gradient=nib.draw.LinearGradient(
        start=(0, 0),
        end=(100, 100),
        colors=[nib.Color.RED, nib.Color.BLUE],
    ),
    style=nib.draw.PaintStyle.FILL,
    opacity=0.8,
)
```

---

## PaintStyle

Determines whether a shape is filled, stroked, or both.

| Value | Description |
|-------|-------------|
| `FILL` | Fill the interior of the shape. Default. |
| `STROKE` | Draw only the outline of the shape. |

---

## StrokeCap

Controls the shape at the ends of open line segments.

| Value | Description |
|-------|-------------|
| `BUTT` | Flat end, no extension beyond the endpoint. Default. |
| `ROUND` | Semicircular end extending beyond the endpoint by half the stroke width. |
| `SQUARE` | Flat end extending beyond the endpoint by half the stroke width. |

---

## StrokeJoin

Controls the shape at corners where two line segments meet.

| Value | Description |
|-------|-------------|
| `MITER` | Sharp corner. Default. Falls back to bevel if the angle is too acute (see `stroke_miter_limit`). |
| `ROUND` | Rounded corner. |
| `BEVEL` | Flat corner, cutting the joint diagonally. |

---

## PointMode

Determines how a list of points is interpreted by the `Points` draw command.

| Value | Description |
|-------|-------------|
| `POINTS` | Draw each point as an individual dot. |
| `LINES` | Draw lines between consecutive pairs of points. |
| `POLYGON` | Draw connected line segments through all points. |

---

## LinearGradient

A linear gradient fill that transitions colors along a straight line.

### Constructor

```python
nib.draw.LinearGradient(start, end, colors, stops=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start` | `tuple[float, float]` | *required* | Starting point `(x, y)` of the gradient in pixel coordinates. |
| `end` | `tuple[float, float]` | *required* | Ending point `(x, y)` of the gradient in pixel coordinates. |
| `colors` | `list[str \| Color]` | *required* | List of colors. Minimum two. |
| `stops` | `list[float]` | `None` | Optional stop positions from 0.0 to 1.0. Must match the length of `colors`. Evenly distributed when omitted. |

### Example

```python
nib.draw.LinearGradient(
    start=(0, 0),
    end=(200, 200),
    colors=["#FF0000", "#00FF00", "#0000FF"],
    stops=[0.0, 0.5, 1.0],
)
```

---

## RadialGradient

A radial gradient fill that transitions colors outward from a center point.

### Constructor

```python
nib.draw.RadialGradient(center, radius, colors, stops=None, focus=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `center` | `tuple[float, float]` | *required* | Center point `(x, y)` of the gradient in pixels. |
| `radius` | `float` | *required* | Radius of the gradient in pixels. |
| `colors` | `list[str \| Color]` | *required* | List of colors. Minimum two. |
| `stops` | `list[float]` | `None` | Optional stop positions from 0.0 to 1.0. |
| `focus` | `tuple[float, float]` | `None` | Optional focus point `(x, y)` for off-center gradients. |

### Example

```python
nib.draw.RadialGradient(
    center=(100, 100),
    radius=80,
    colors=[nib.Color.YELLOW, nib.Color.RED],
)
```

---

## SweepGradient

A sweep (conic/angular) gradient that transitions colors around a center point.

### Constructor

```python
nib.draw.SweepGradient(center, colors, stops=None, start_angle=0, end_angle=6.283)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `center` | `tuple[float, float]` | *required* | Center point `(x, y)` of the gradient. |
| `colors` | `list[str \| Color]` | *required* | List of colors. |
| `stops` | `list[float]` | `None` | Optional stop positions from 0.0 to 1.0. |
| `start_angle` | `float` | `0` | Starting angle in radians. |
| `end_angle` | `float` | `6.283` | Ending angle in radians (default is 2 * pi, a full circle). |

### Example

```python
# Color wheel
nib.draw.SweepGradient(
    center=(100, 100),
    colors=[nib.Color.RED, nib.Color.GREEN, nib.Color.BLUE, nib.Color.RED],
)
```

---

## Blur

A blur effect that can be applied via the `Paint.blur` parameter.

### Constructor

```python
nib.draw.Blur(sigma_x, sigma_y=None, style="normal")
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sigma_x` | `float` | *required* | Horizontal blur radius. |
| `sigma_y` | `float` | `None` | Vertical blur radius. Defaults to `sigma_x` if not specified. |
| `style` | `str` | `"normal"` | Blur style: `"normal"`, `"solid"`, `"outer"`, or `"inner"`. |

### Example

```python
paint = nib.draw.Paint(
    color="#000000",
    blur=nib.draw.Blur(sigma_x=5),
)
```
