# Capsule

A pill-shaped rectangle where the shorter dimension is completely rounded. Capsules are commonly used for buttons, tags, badges, and other UI elements that need a smooth, rounded appearance.

For horizontal capsules (width > height), the ends are semicircles with radius equal to half the height. For vertical capsules (height > width), the ends are semicircles with radius equal to half the width. This differs from `Rectangle` with `corner_radius`, which uses a fixed corner radius regardless of dimensions.

## Constructor

```python
nib.Capsule(
    fill=None,
    stroke_color=None,
    stroke_width=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fill` | `str \| Color` | `None` | Fill color for the capsule interior. Accepts hex strings, named colors, or `Color` instances. |
| `stroke_color` | `str \| Color` | `None` | Stroke color for the capsule border. |
| `stroke_width` | `float` | `None` | Width of the stroke in points. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, `animation`, etc. |

## Examples

### Basic capsule shapes

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Horizontal capsule
                nib.Capsule(fill=nib.Color.BLUE, width=150, height=50),
                # Vertical capsule
                nib.Capsule(fill=nib.Color.GREEN, width=40, height=120),
                # Capsule with stroke
                nib.Capsule(
                    fill=nib.Color.PURPLE,
                    stroke_color=nib.Color.WHITE,
                    stroke_width=2,
                    width=120,
                    height=40,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### Tag / badge with capsule background

Use a Capsule as the background for text to create pill-shaped labels.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Text(
                    "NEW",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.WHITE,
                    padding={"horizontal": 10, "vertical": 4},
                    background=nib.Capsule(fill=nib.Color.RED),
                ),
                nib.Text(
                    "SALE",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.WHITE,
                    padding={"horizontal": 10, "vertical": 4},
                    background=nib.Capsule(fill=nib.Color.GREEN),
                ),
                nib.Text(
                    "HOT",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.WHITE,
                    padding={"horizontal": 10, "vertical": 4},
                    background=nib.Capsule(fill=nib.Color.ORANGE),
                ),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Capsule as clip shape

Clip an image into a capsule shape for a banner-style appearance.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Image(
                    url="https://example.com/banner.jpg",
                    width=200,
                    height=60,
                    clip_shape=nib.Capsule(),
                ),
                nib.Text("Clipped to capsule shape"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
