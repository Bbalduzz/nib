# Ellipse

An oval shape that stretches to fill its frame with independent width and height dimensions. Unlike `Circle` which maintains a 1:1 aspect ratio, Ellipse can have different width and height values, creating an oval shape.

When width equals height, an Ellipse appears identical to a Circle.

## Constructor

```python
nib.Ellipse(
    fill=None,
    stroke_color=None,
    stroke_width=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fill` | `str \| Color` | `None` | Fill color for the ellipse interior. Accepts hex strings, named colors, or `Color` instances. |
| `stroke_color` | `str \| Color` | `None` | Stroke color for the ellipse border. |
| `stroke_width` | `float` | `None` | Width of the stroke in points. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, `animation`, etc. |

## Examples

### Basic ellipses

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Wide ellipse
                nib.Ellipse(fill=nib.Color.BLUE, width=150, height=80),
                # Tall ellipse
                nib.Ellipse(fill=nib.Color.PURPLE, width=80, height=150),
                # Ellipse with stroke
                nib.Ellipse(
                    fill=nib.Color.ORANGE,
                    stroke_color=nib.Color.WHITE,
                    stroke_width=2,
                    width=120,
                    height=60,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### Ellipse as background

Use an Ellipse as a decorative background for text badges.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text(
                    "Badge",
                    foreground_color=nib.Color.WHITE,
                    font=nib.Font.CAPTION,
                    padding={"horizontal": 16, "vertical": 8},
                    background=nib.Ellipse(fill=nib.Color.RED),
                ),
            ],
            padding=16,
        )
    )

nib.run(main)
```

### Decorative oval ring

Create a stroke-only ellipse for decorative purposes.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Ellipse(
                    stroke_color="#4ECDC4",
                    stroke_width=3,
                    width=200,
                    height=120,
                    opacity=0.5,
                ),
                nib.Ellipse(
                    stroke_color="#FF6B6B",
                    stroke_width=3,
                    width=160,
                    height=90,
                    opacity=0.5,
                ),
                nib.Text("Centered", font=nib.Font.HEADLINE),
            ],
            padding=16,
        )
    )

nib.run(main)
```
