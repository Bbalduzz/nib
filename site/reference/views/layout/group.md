# Group

A transparent container that groups multiple views together without adding any visual structure or layout behavior. Group does not impose positioning or spacing on its children, unlike VStack, HStack, or other layout containers.

Common use cases include applying modifiers to multiple views at once, returning multiple views from conditional expressions, and organizing code without affecting visual output.

## Constructor

```python
nib.Group(
    controls=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to group together. The views are rendered without any additional layout structure imposed by the group itself. |
| `**modifiers` | | | Common view modifiers applied to the group as a whole, affecting all children: `padding`, `background`, `foreground_color`, `opacity`, `font`, etc. |

## Examples

### Shared styling

Apply a single modifier to multiple views at once by wrapping them in a Group.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Group(
                    controls=[
                        nib.Text("Important"),
                        nib.Text("Information"),
                    ],
                    foreground_color=nib.Color.RED,
                ),
                nib.Text("Normal text"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Conditional content

Use Group to return multiple views from a conditional branch where a single parent is required.

```python
import nib

def main(app: nib.App):
    show_details = True

    if show_details:
        content = nib.Group(
            controls=[
                nib.Text("Title", font=nib.Font.HEADLINE),
                nib.Text("Subtitle"),
                nib.Text("Description"),
            ],
        )
    else:
        content = nib.Text("Title only")

    app.build(
        nib.VStack(
            controls=[content],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Shared opacity

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Group(
                    controls=[
                        nib.Image(system_name="star.fill"),
                        nib.Text("Favorite"),
                    ],
                    opacity=0.5,
                ),
                nib.Text("Full opacity text"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
