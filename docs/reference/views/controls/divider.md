# Divider

![Divider control](../../../assets/img/controls/divider.png)

A thin visual separator line used to organize content into sections. In a `VStack`, the divider appears as a horizontal line. In an `HStack`, it appears as a vertical line. The divider automatically sizes itself to fit its container.

Divider has no view-specific parameters -- it accepts only common view modifiers.

## Constructor

```python
nib.Divider(**modifiers)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `**modifiers` | | | Common view modifiers. Commonly used: `foreground_color` (line color), `padding` (space around the divider), `opacity` (transparency). |

## Examples

### Basic section divider

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Text("Section 1"),
            nib.Divider(),
            nib.Text("Section 2"),
            nib.Divider(),
            nib.Text("Section 3"),
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Styled divider with color and spacing

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Text("Header", style=nib.TextStyle.TITLE),
            nib.Divider(
                foreground_color=nib.Color.BLUE,
                padding={"vertical": 8},
            ),
            nib.Text("Content goes below the divider."),
        ], spacing=4, padding=16)
    )

nib.run(main)
```

### Subtle list separator

```python
import nib

def main(app: nib.App):
    items = ["Apple", "Banana", "Cherry", "Date"]
    controls = []
    for i, item in enumerate(items):
        controls.append(nib.Text(item, padding={"vertical": 4}))
        if i < len(items) - 1:
            controls.append(
                nib.Divider(foreground_color="#E0E0E0", opacity=0.6)
            )

    app.build(
        nib.VStack(controls=controls, spacing=0, padding=16)
    )

nib.run(main)
```
