# Gradients

Gradient views create smooth color transitions that can be used as standalone views, backgrounds, or fills for custom shapes. Nib provides four gradient types: `LinearGradient`, `RadialGradient`, `AngularGradient`, and `EllipticalGradient`.

All gradients accept either a `colors` list (evenly distributed) or a `stops` list (explicit position control). Use one or the other, not both.

## LinearGradient

Colors transition along a straight line from a start point to an end point. Points are specified in unit coordinates where `(0, 0)` is top-left and `(1, 1)` is bottom-right.

### Constructor

```python
nib.LinearGradient(
    colors=None,
    stops=None,
    start=(0.5, 0),
    end=(0.5, 1),
    **modifiers,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `colors` | `list[str \| Color]` | `None` | Colors for the gradient, evenly distributed. Use this or `stops`, not both. |
| `stops` | `list[tuple[float, str]]` | `None` | List of `(position, color)` tuples for explicit control. Positions are 0.0 to 1.0. |
| `start` | `tuple[float, float]` | `(0.5, 0)` | Start point in unit coordinates. Default is top-center. |
| `end` | `tuple[float, float]` | `(0.5, 1)` | End point in unit coordinates. Default is bottom-center. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, etc. |

## RadialGradient

Colors radiate outward from a center point in a circular pattern.

### Constructor

```python
nib.RadialGradient(
    colors=None,
    stops=None,
    center=(0.5, 0.5),
    start_radius=0,
    end_radius=100,
    **modifiers,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `colors` | `list[str \| Color]` | `None` | Colors for the gradient, evenly distributed. |
| `stops` | `list[tuple[float, str]]` | `None` | List of `(position, color)` tuples for explicit control. |
| `center` | `tuple[float, float]` | `(0.5, 0.5)` | Center point in unit coordinates. |
| `start_radius` | `float` | `0` | Inner radius where the gradient begins, in points. |
| `end_radius` | `float` | `100` | Outer radius where the gradient ends, in points. |
| `**modifiers` | | | Common view modifiers. |

## AngularGradient

Colors rotate around a center point, creating a color wheel or conic gradient effect.

### Constructor

```python
nib.AngularGradient(
    colors=None,
    stops=None,
    center=(0.5, 0.5),
    start_angle=0,
    end_angle=360,
    **modifiers,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `colors` | `list[str \| Color]` | `None` | Colors for the gradient, evenly distributed. |
| `stops` | `list[tuple[float, str]]` | `None` | List of `(position, color)` tuples for explicit control. |
| `center` | `tuple[float, float]` | `(0.5, 0.5)` | Center point in unit coordinates. |
| `start_angle` | `float` | `0` | Starting angle in degrees. |
| `end_angle` | `float` | `360` | Ending angle in degrees. |
| `**modifiers` | | | Common view modifiers. |

## EllipticalGradient

Colors radiate outward in an elliptical pattern that stretches to fill the view's frame, creating an elliptical pattern rather than circular.

### Constructor

```python
nib.EllipticalGradient(
    colors=None,
    stops=None,
    center=(0.5, 0.5),
    start_radius_fraction=0,
    end_radius_fraction=0.5,
    **modifiers,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `colors` | `list[str \| Color]` | `None` | Colors for the gradient, evenly distributed. |
| `stops` | `list[tuple[float, str]]` | `None` | List of `(position, color)` tuples for explicit control. |
| `center` | `tuple[float, float]` | `(0.5, 0.5)` | Center point in unit coordinates. |
| `start_radius_fraction` | `float` | `0` | Fraction of the view size where the gradient starts. |
| `end_radius_fraction` | `float` | `0.5` | Fraction of the view size where the gradient ends. |
| `**modifiers` | | | Common view modifiers. |

## Examples

### Linear gradient background

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Gradient Background", font=nib.Font.TITLE,
                         foreground_color=nib.Color.WHITE),
            ],
            padding=32,
            background=nib.LinearGradient(
                colors=["#667eea", "#764ba2"],
                start=(0, 0),
                end=(1, 1),
            ),
        )
    )

nib.run(main)
```

### Gradient with explicit stops

Control exactly where each color appears using stops.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Linear with stops
                nib.LinearGradient(
                    stops=[
                        (0.0, "#FF0000"),
                        (0.3, "#FFFF00"),
                        (0.7, "#00FF00"),
                        (1.0, "#0000FF"),
                    ],
                    start=(0, 0.5),
                    end=(1, 0.5),
                    height=60,
                    corner_radius=8,
                ),
                # Radial gradient
                nib.RadialGradient(
                    colors=["#FFFFFF", "#000000"],
                    center=(0.5, 0.5),
                    start_radius=0,
                    end_radius=120,
                    width=200,
                    height=200,
                    corner_radius=8,
                ),
            ],
            spacing=16,
            padding=16,
        )
    )

nib.run(main)
```

### Angular color wheel

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.AngularGradient(
                    colors=[
                        "#FF0000", "#FF8000", "#FFFF00",
                        "#00FF00", "#00FFFF", "#0000FF",
                        "#8000FF", "#FF0080", "#FF0000",
                    ],
                    center=(0.5, 0.5),
                    width=200,
                    height=200,
                    clip_shape=nib.Circle(),
                ),
                nib.Text("Color Wheel", font=nib.Font.CAPTION),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
