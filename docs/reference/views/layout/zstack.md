# ZStack

A layered stack layout that overlays its child views on top of each other along the z-axis. The first child in the `controls` list is rendered at the back (bottom layer), and each subsequent child is layered on top.

Unlike VStack and HStack which arrange children sequentially, ZStack allows children to occupy the same space. This is useful for creating backgrounds, overlays, badges, and complex layered UI elements.

## Constructor

```python
nib.ZStack(
    controls=None,
    alignment=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to layer on top of each other. The first view is at the back, subsequent views are layered on top. |
| `alignment` | `Alignment \| str` | `None` | Two-dimensional alignment of children within the stack. Options: `Alignment.CENTER`, `Alignment.TOP`, `Alignment.BOTTOM`, `Alignment.LEADING`, `Alignment.TRAILING`, `Alignment.TOP_LEADING`, `Alignment.TOP_TRAILING`, `Alignment.BOTTOM_LEADING`, `Alignment.BOTTOM_TRAILING`. Defaults to center. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, `on_hover`, `on_click`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `controls` | `list[View]` | Get or set the child views. Setting triggers a UI update. |

## Examples

### Card with background

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Rectangle(corner_radius=12, fill="#1a1a1a"),
                nib.VStack(
                    controls=[
                        nib.Text("Card Title", font=nib.Font.HEADLINE),
                        nib.Text("Card content goes here"),
                    ],
                    spacing=8,
                    padding=16,
                ),
            ],
        )
    )

nib.run(main)
```

### Badge overlay

Position a notification badge in the top-trailing corner of an icon.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Image(system_name="bell.fill", width=32, height=32),
                nib.Circle(fill=nib.Color.RED, width=12, height=12),
            ],
            alignment=nib.Alignment.TOP_TRAILING,
            padding=16,
        )
    )

nib.run(main)
```

### Image with gradient overlay

Layer a semi-transparent overlay and text caption on top of an image.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Image(url="https://example.com/photo.jpg", width=300, height=200),
                nib.Rectangle(fill=nib.Color.BLACK, opacity=0.3),
                nib.Text(
                    "Photo Caption",
                    foreground_color=nib.Color.WHITE,
                    font=nib.Font.HEADLINE,
                ),
            ],
            alignment=nib.Alignment.BOTTOM,
        )
    )

nib.run(main)
```
