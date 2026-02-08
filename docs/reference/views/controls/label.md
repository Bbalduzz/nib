# Label

![Label control](../../../assets/img/controls/label.png)

A view that combines an SF Symbol icon with a text title, following Apple's Human Interface Guidelines. Labels are commonly used in navigation items, list rows, and menu entries. For full control over appearance, custom views can be provided instead of strings.

## Constructor

```python
nib.Label(
    title=None,
    icon=None,
    title_view=None,
    icon_view=None,
    style=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | `None` | Text string displayed as the label title. For custom styling, use `title_view` instead. |
| `icon` | `str` | `None` | SF Symbol name for the icon (e.g., `"gear"`, `"star.fill"`, `"bell.badge"`). For custom icons, use `icon_view` instead. |
| `title_view` | `View` | `None` | Custom view to use as the title. Alternative to `title`. |
| `icon_view` | `View` | `None` | Custom view to use as the icon. Alternative to `icon`. |
| `style` | `LabelStyle \| str` | `None` | Determines which parts of the label are shown. Options: `LabelStyle.automatic`, `LabelStyle.titleOnly`, `LabelStyle.iconOnly`, `LabelStyle.titleAndIcon`. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `font`, `opacity`, etc. |

## Examples

### Basic label with icon

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Label("Settings", icon="gear"),
            nib.Label("Favorites", icon="star.fill",
                       foreground_color=nib.Color.YELLOW),
            nib.Label("Notifications", icon="bell.badge"),
        ], spacing=12, padding=16)
    )

nib.run(main)
```

### Label style variations

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Label("Title and Icon", icon="person.fill",
                       style=nib.LabelStyle.titleAndIcon),
            nib.Label("Title Only", icon="person.fill",
                       style=nib.LabelStyle.titleOnly),
            nib.Label("Icon Only", icon="person.fill",
                       style=nib.LabelStyle.iconOnly),
        ], spacing=12, padding=16)
    )

nib.run(main)
```

### Label with custom content views

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Label(
            title_view=nib.Text("Premium",
                                 font=nib.Font.HEADLINE,
                                 foreground_color=nib.Color.YELLOW),
            icon_view=nib.Image(system_name="crown.fill",
                                 foreground_color=nib.Color.YELLOW),
            padding=16,
        )
    )

nib.run(main)
```
