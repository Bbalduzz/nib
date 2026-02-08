# Form

![Form](../../../assets/img/controls/form.png)

A container for grouping data-entry controls. On macOS, Form typically displays as a two-column layout with labels on the left and controls on the right, providing a clean and consistent appearance for settings and preferences interfaces.

Form supports different visual styles and works well with `Section` for organizing controls into groups.

## Constructor

```python
nib.Form(
    controls=None,
    style=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to display within the form. Typically includes controls like `Toggle`, `Picker`, `TextField`, `Slider`, and `Section` for grouping. |
| `style` | `FormStyle \| str` | `None` | The visual style for the form. Options: `FormStyle.AUTOMATIC` (platform default), `FormStyle.COLUMNS` (two-column layout, macOS default), `FormStyle.GROUPED` (grouped sections with visual separation). |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Examples

### Basic settings form

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Form(
            controls=[
                nib.Toggle("Enable notifications", is_on=True),
                nib.Picker("Language", selection="en", options=["en", "es", "fr"]),
                nib.TextField(value="", placeholder="Username"),
            ],
            style=nib.FormStyle.COLUMNS,
            padding=16,
        )
    )

nib.run(main)
```

### Form with grouped sections

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Form(
            controls=[
                nib.Section(
                    controls=[
                        nib.Toggle("Dark Mode", is_on=False),
                        nib.Picker(
                            "Accent Color",
                            selection="blue",
                            options=["blue", "purple", "green", "orange"],
                        ),
                    ],
                    header="Appearance",
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
            style=nib.FormStyle.GROUPED,
        )
    )

nib.run(main)
```

### Preferences form with slider

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Form(
            controls=[
                nib.Toggle("Auto-save", is_on=True),
                nib.Toggle("Launch at login", is_on=False),
                nib.Picker(
                    "Update frequency",
                    selection="weekly",
                    options=["daily", "weekly", "monthly"],
                ),
                nib.Slider("Volume", value=0.8, min_value=0, max_value=1),
            ],
            style=nib.FormStyle.COLUMNS,
            padding=16,
        )
    )

nib.run(main)
```
