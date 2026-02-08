# HStack

A horizontal stack layout that arranges its child views from leading to trailing (left to right in left-to-right locales). HStack is one of the primary layout containers in Nib, commonly used for toolbars, icon-label pairs, and side-by-side content.

Children are rendered in the order they appear in the `controls` list, with optional spacing between them and configurable vertical alignment.

## Constructor

```python
nib.HStack(
    controls=None,
    spacing=None,
    alignment=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to arrange horizontally, rendered from leading to trailing. |
| `spacing` | `float` | `None` | Distance in points between adjacent child views. When `None`, the system default spacing is used. |
| `alignment` | `VerticalAlignment \| str` | `None` | Vertical alignment of children within the stack. Options: `VerticalAlignment.TOP`, `VerticalAlignment.CENTER`, `VerticalAlignment.BOTTOM`. Defaults to center. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, `on_drop`, `on_hover`, `on_click`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `controls` | `list[View]` | Get or set the child views. Setting triggers a UI update. |

## Examples

### Icon with label

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Image(system_name="star.fill"),
                nib.Text("Favorites"),
            ],
            spacing=8,
            alignment=nib.VerticalAlignment.CENTER,
            padding=12,
        )
    )

nib.run(main)
```

### Toolbar with spacers

Use `Spacer` to push elements to opposite edges. Multiple spacers divide available space equally.

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
            spacing=8,
            padding={"horizontal": 16, "vertical": 8},
        )
    )

nib.run(main)
```

### Nested stacks

Combine HStack and VStack to create more complex layouts.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.HStack(
            controls=[
                nib.Image(system_name="person.fill", width=40, height=40),
                nib.VStack(
                    controls=[
                        nib.Text("Username", font=nib.Font.HEADLINE),
                        nib.Text("Online", foreground_color=nib.Color.SECONDARY),
                    ],
                    alignment=nib.HorizontalAlignment.LEADING,
                    spacing=2,
                ),
            ],
            spacing=12,
            alignment=nib.VerticalAlignment.CENTER,
            padding=16,
        )
    )

nib.run(main)
```
