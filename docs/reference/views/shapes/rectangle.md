# Rectangle

A rectangular shape with configurable corner radii. Rectangle can have sharp corners (default), uniform rounded corners via a single float, or per-corner control using `CornerRadius`.

When `corner_radius` is provided, Rectangle behaves as a rounded rectangle. For full per-corner control, pass a `CornerRadius` instance.

## Constructor

```python
nib.Rectangle(
    fill=None,
    corner_radius=None,
    stroke_color=None,
    stroke_width=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fill` | `str \| Color` | `None` | Fill color for the rectangle interior. Accepts hex strings (`"#FF5733"`), named colors (`"red"`), or `Color` instances. |
| `corner_radius` | `float \| CornerRadius` | `None` | Corner rounding. A float applies a uniform radius to all corners. A `CornerRadius` instance provides per-corner control. `None` produces sharp corners. |
| `stroke_color` | `str \| Color` | `None` | Stroke color for the rectangle border. |
| `stroke_width` | `float` | `None` | Width of the stroke in points. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, `animation`, etc. |

## CornerRadius

For per-corner control, use `nib.CornerRadius`:

```python
nib.CornerRadius(
    top_left=0,
    top_right=0,
    bottom_left=0,
    bottom_right=0,
)
```

Factory methods:

| Method | Description |
|--------|-------------|
| `CornerRadius.all(radius)` | Uniform radius for all corners. |
| `CornerRadius.vertical(top, bottom)` | Same radius for top corners and bottom corners. |
| `CornerRadius.only(**corners)` | Set only specific corners, others default to 0. |

## Examples

### Basic shapes

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                # Sharp corners
                nib.Rectangle(fill=nib.Color.BLUE, width=80, height=80),
                # Rounded corners
                nib.Rectangle(
                    fill=nib.Color.GREEN,
                    corner_radius=12,
                    width=80,
                    height=80,
                ),
                # With stroke
                nib.Rectangle(
                    fill=nib.Color.GRAY,
                    corner_radius=8,
                    stroke_color=nib.Color.WHITE,
                    stroke_width=2,
                    width=80,
                    height=80,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### Per-corner radius

Round only the top corners to create a card header shape.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Rectangle(
                    fill="#3B82F6",
                    corner_radius=nib.CornerRadius(
                        top_left=16,
                        top_right=16,
                        bottom_left=0,
                        bottom_right=0,
                    ),
                    width=200,
                    height=60,
                ),
                nib.Rectangle(
                    fill="#1E293B",
                    corner_radius=nib.CornerRadius.vertical(top=0, bottom=16),
                    width=200,
                    height=100,
                ),
            ],
            spacing=0,
        )
    )

nib.run(main)
```

### Rectangle as background

Pass a Rectangle (with or without rounded corners) as the `background` modifier for any view.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Card content", font=nib.Font.HEADLINE),
                nib.Text("Some details here", foreground_color=nib.Color.SECONDARY),
            ],
            spacing=8,
            padding=16,
            background=nib.Rectangle(
                fill="#262626",
                corner_radius=12,
                stroke_color="#383837",
                stroke_width=1,
            ),
        )
    )

nib.run(main)
```
