# VStack

A vertical stack layout that arranges its child views from top to bottom. VStack is one of the primary layout containers in Nib and is used to build most vertical interfaces.

Children are rendered in the order they appear in the `controls` list, with optional spacing between them and configurable horizontal alignment.

## Constructor

```python
nib.VStack(
    controls=None,
    spacing=None,
    alignment=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to arrange vertically, rendered from top to bottom. |
| `spacing` | `float` | `None` | Distance in points between adjacent child views. When `None`, the system default spacing is used. |
| `alignment` | `HorizontalAlignment \| str` | `None` | Horizontal alignment of children within the stack. Options: `HorizontalAlignment.LEADING`, `HorizontalAlignment.CENTER`, `HorizontalAlignment.TRAILING`. Defaults to center. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, `on_drop`, `on_hover`, `on_click`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `controls` | `list[View]` | Get or set the child views. Setting triggers a UI update. |

## Examples

### Basic vertical layout

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("First"),
                nib.Text("Second"),
                nib.Text("Third"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Left-aligned stack with styling

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Title", font=nib.Font.TITLE),
                nib.Text("Subtitle", foreground_color=nib.Color.SECONDARY),
                nib.Button("Action", action=lambda: print("tapped")),
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=12,
            padding=16,
            background=nib.Rectangle(
                corner_radius=8,
                fill="#333333",
            ),
        )
    )

nib.run(main)
```

### Drag and drop

VStack supports file drag-and-drop through the `on_drop` modifier. The callback receives a list of file paths.

```python
import nib

def main(app: nib.App):
    status = nib.Text("Drop files here")

    def handle_drop(paths):
        status.content = f"Received {len(paths)} file(s)"

    app.build(
        nib.VStack(
            controls=[status],
            spacing=8,
            padding=24,
            on_drop=handle_drop,
            background="#1a1a1a",
            corner_radius=12,
        )
    )

nib.run(main)
```
