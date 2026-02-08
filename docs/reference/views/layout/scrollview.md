# ScrollView

A scrollable container that allows content to exceed the visible bounds. ScrollView supports vertical, horizontal, or bidirectional scrolling with optional scroll indicators.

The scroll view automatically determines the content size based on its children and enables scrolling when the content exceeds the available space.

## Constructor

```python
nib.ScrollView(
    controls=None,
    axes="vertical",
    shows_indicators=True,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views to display in the scrollable region. The content size is determined by the combined size of all children. |
| `axes` | `str` | `"vertical"` | The scroll direction. Options: `"vertical"` (up/down), `"horizontal"` (left/right), `"both"` (bidirectional). |
| `shows_indicators` | `bool` | `True` | Whether to display scroll indicators (scrollbars). Set to `False` for a cleaner appearance when indicators are not needed. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Examples

### Vertical scrollable list

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[nib.Text(f"Item {i}") for i in range(50)],
                    spacing=4,
                ),
            ],
            height=300,
            padding=8,
        )
    )

nib.run(main)
```

### Horizontal scrolling gallery

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ScrollView(
            controls=[
                nib.HStack(
                    controls=[
                        nib.Rectangle(
                            corner_radius=8,
                            fill=color,
                            width=100,
                            height=100,
                        )
                        for color in ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
                    ],
                    spacing=8,
                ),
            ],
            axes="horizontal",
            shows_indicators=False,
            padding=16,
        )
    )

nib.run(main)
```

### Scrollable form

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        nib.TextField(value="", placeholder="Name"),
                        nib.TextField(value="", placeholder="Email"),
                        nib.TextField(value="", placeholder="Subject"),
                        nib.TextEditor(value="", placeholder="Message"),
                        nib.Button("Submit", action=lambda: print("submitted")),
                    ],
                    spacing=12,
                    padding=16,
                ),
            ],
            axes="vertical",
            shows_indicators=True,
            height=400,
        )
    )

nib.run(main)
```
