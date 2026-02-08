# BlendMode

The `BlendMode` enum controls how a view is composited with the content behind it. It maps directly to SwiftUI's `.blendMode()` view modifier.

```python
import nib

nib.Image(source="overlay.png", blend_mode=nib.BlendMode.MULTIPLY)
```

## Values

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `BlendMode.NORMAL` | `.normal` | No blending (default). The source view completely covers content behind it. |
| `BlendMode.MULTIPLY` | `.multiply` | Multiplies the source and destination colors. Always produces darker results. |
| `BlendMode.SCREEN` | `.screen` | Inverts, multiplies, and inverts again. Always produces lighter results. |
| `BlendMode.OVERLAY` | `.overlay` | Combines multiply and screen. Light areas get lighter, dark areas get darker. |
| `BlendMode.DARKEN` | `.darken` | Selects the darker of the source and destination colors per channel. |
| `BlendMode.LIGHTEN` | `.lighten` | Selects the lighter of the source and destination colors per channel. |
| `BlendMode.COLOR_DODGE` | `.colorDodge` | Brightens the destination color to reflect the source. |
| `BlendMode.COLOR_BURN` | `.colorBurn` | Darkens the destination color to reflect the source. |
| `BlendMode.SOFT_LIGHT` | `.softLight` | A softer version of overlay. |
| `BlendMode.HARD_LIGHT` | `.hardLight` | Similar to overlay but with the source and destination roles swapped. |
| `BlendMode.DIFFERENCE` | `.difference` | Subtracts the darker color from the lighter one. |
| `BlendMode.EXCLUSION` | `.exclusion` | Similar to difference but with lower contrast. |
| `BlendMode.HUE` | `.hue` | Uses the hue of the source with the saturation and luminosity of the destination. |
| `BlendMode.SATURATION` | `.saturation` | Uses the saturation of the source with the hue and luminosity of the destination. |
| `BlendMode.COLOR` | `.color` | Uses the hue and saturation of the source with the luminosity of the destination. |
| `BlendMode.LUMINOSITY` | `.luminosity` | Uses the luminosity of the source with the hue and saturation of the destination. |

## Usage

Pass a `BlendMode` value to the `blend_mode` parameter on any view:

```python
nib.Rectangle(fill=nib.Color.BLUE, blend_mode=nib.BlendMode.OVERLAY)
```

You can also pass a string:

```python
nib.Rectangle(fill=nib.Color.BLUE, blend_mode="overlay")
```

## Examples

### Color overlay on an image

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Image(source="photo.jpg", width=300, height=200),
                nib.Rectangle(
                    fill=nib.Color.BLUE.with_opacity(0.4),
                    width=300,
                    height=200,
                    blend_mode=nib.BlendMode.OVERLAY,
                ),
            ],
        )
    )

nib.run(main)
```

### Layered shapes with blend modes

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Circle(fill=nib.Color.RED, width=120, height=120),
                nib.Circle(
                    fill=nib.Color.BLUE,
                    width=120,
                    height=120,
                    offset=nib.Offset(40, 0),
                    blend_mode=nib.BlendMode.SCREEN,
                ),
                nib.Circle(
                    fill=nib.Color.GREEN,
                    width=120,
                    height=120,
                    offset=nib.Offset(20, 35),
                    blend_mode=nib.BlendMode.SCREEN,
                ),
            ],
            padding=40,
        )
    )

nib.run(main)
```
