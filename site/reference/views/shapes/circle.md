# Circle

A circular shape centered in its frame. Circle always maintains a 1:1 aspect ratio, filling the smaller dimension of its frame.

Circle supports trim properties for drawing partial arcs, making it useful for progress rings and arc indicators. Values for `trim_from` and `trim_to` range from 0.0 to 1.0, where 0.0 is the 3 o'clock position and 1.0 is a full circle. Use `rotation` to change the starting position (for example, -90 to start from the top).

## Constructor

```python
nib.Circle(
    fill=None,
    stroke_color=None,
    stroke_width=None,
    trim_from=None,
    trim_to=None,
    rotation=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fill` | `str \| Color` | `None` | Fill color for the circle interior. Accepts hex strings, named colors, or `Color` instances. |
| `stroke_color` | `str \| Color` | `None` | Stroke color for the circle border. |
| `stroke_width` | `float` | `None` | Width of the stroke in points. |
| `trim_from` | `float` | `None` | Fractional starting point (0.0 to 1.0) for partial circle arcs. |
| `trim_to` | `float` | `None` | Fractional ending point (0.0 to 1.0) for partial circle arcs. |
| `rotation` | `float` | `None` | Rotation angle in degrees. Use -90 to start trimmed circles from the top instead of the right. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, `animation`, etc. |

## Examples

### Basic circles

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                # Filled circle
                nib.Circle(fill=nib.Color.BLUE, width=60, height=60),
                # Circle with stroke
                nib.Circle(
                    fill=nib.Color.RED,
                    stroke_color=nib.Color.WHITE,
                    stroke_width=2,
                    width=60,
                    height=60,
                ),
                # Stroke-only circle
                nib.Circle(
                    stroke_color=nib.Color.GREEN,
                    stroke_width=3,
                    width=60,
                    height=60,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### Progress ring

Use `trim_from` and `trim_to` to create a progress indicator. Set `rotation=-90` to start from the top.

```python
import nib

def main(app: nib.App):
    progress = 0.75

    app.build(
        nib.ZStack(
            controls=[
                # Background track
                nib.Circle(
                    stroke_color="#333333",
                    stroke_width=8,
                    width=100,
                    height=100,
                ),
                # Progress arc
                nib.Circle(
                    stroke_color=nib.Color.BLUE,
                    stroke_width=8,
                    trim_from=0.0,
                    trim_to=progress,
                    rotation=-90,
                    width=100,
                    height=100,
                ),
                # Label
                nib.Text(f"{int(progress * 100)}%", font=nib.Font.HEADLINE),
            ],
            padding=16,
        )
    )

nib.run(main)
```

### Circle as clip shape

Clip an image into a circular shape.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Image(
                    url="https://example.com/avatar.jpg",
                    width=80,
                    height=80,
                    clip_shape=nib.Circle(),
                ),
                nib.Text("Username", font=nib.Font.HEADLINE),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
