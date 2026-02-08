# Spacer

A flexible space that expands to fill available room within a stack layout. Spacer is a layout primitive that takes up as much space as available in its parent HStack or VStack.

In an HStack, Spacer expands horizontally. In a VStack, it expands vertically. When multiple spacers are present, they divide the available space equally. This makes Spacer essential for creating flexible layouts where elements need to be pushed apart or distributed evenly.

## Constructor

```python
nib.Spacer(
    min_length=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_length` | `float` | `None` | Minimum length in points that the spacer must occupy, even when space is limited. Useful for ensuring minimum gaps between elements. |
| `**modifiers` | | | Common view modifiers. While spacers typically do not need visual styling, frame constraints can still be applied. |

## Examples

### Push content to edges

Use a Spacer to push elements to opposite sides of a horizontal stack.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Text("Left"),
                nib.Spacer(),
                nib.Text("Right"),
            ],
            padding=16,
        )
    )

nib.run(main)
```

### Centered title toolbar

Two spacers create equal space on both sides of the title, centering it while pushing the buttons to the edges.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Button("Back", action=lambda: print("back")),
                nib.Spacer(),
                nib.Text("Title", font=nib.Font.HEADLINE),
                nib.Spacer(),
                nib.Button("Done", action=lambda: print("done")),
            ],
            padding={"horizontal": 16, "vertical": 8},
        )
    )

nib.run(main)
```

### Bottom-aligned footer

In a VStack, Spacer pushes subsequent content to the bottom of the container.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Header", font=nib.Font.TITLE),
                nib.Text("Main content goes here"),
                nib.Spacer(min_length=20),
                nib.Text(
                    "Footer",
                    foreground_color=nib.Color.SECONDARY,
                    font=nib.Font.CAPTION,
                ),
            ],
            height=400,
            padding=16,
        )
    )

nib.run(main)
```
