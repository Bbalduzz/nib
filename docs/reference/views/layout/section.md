# Section

![Section](../../../assets/img/controls/section.png)

A container for grouping related content with optional header and footer text. Section is designed to be used within a `List` or `Form` to organize content into logical groups.

The header typically describes the section's purpose, while the footer provides additional context, explanations, or disclaimers.

## Constructor

```python
nib.Section(
    controls=None,
    header=None,
    footer=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to display within the section, rendered between the header and footer. |
| `header` | `str` | `None` | Text displayed above the section content. Rendered in a secondary text style. |
| `footer` | `str` | `None` | Text displayed below the section content. Rendered in a smaller, secondary text style. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Examples

### Section with header

```python
import nib

def main(app: nib.App):
    app.build(
        nib.List(
            controls=[
                nib.Section(
                    controls=[
                        nib.Text("Item 1"),
                        nib.Text("Item 2"),
                        nib.Text("Item 3"),
                    ],
                    header="My Section",
                ),
            ],
            height=300,
        )
    )

nib.run(main)
```

### Section with header and footer

```python
import nib

def main(app: nib.App):
    app.build(
        nib.List(
            controls=[
                nib.Section(
                    controls=[
                        nib.Toggle("Dark Mode", is_on=False),
                        nib.Toggle("Auto-brightness", is_on=True),
                    ],
                    header="Display",
                    footer="Adjust display settings for comfortable viewing.",
                ),
            ],
            height=300,
        )
    )

nib.run(main)
```

### Multiple sections in a form

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Form(
            controls=[
                nib.Section(
                    controls=[
                        nib.TextField(value="", placeholder="Username"),
                        nib.SecureField(value="", placeholder="Password"),
                    ],
                    header="Account",
                ),
                nib.Section(
                    controls=[
                        nib.Toggle("Push notifications", is_on=True),
                        nib.Toggle("Email notifications", is_on=False),
                    ],
                    header="Notifications",
                    footer="Choose how you want to be notified.",
                ),
            ],
            padding=16,
        )
    )

nib.run(main)
```
