# Text

![Text control](../../../assets/img/controls/text.png)

A view that displays one or more lines of read-only text. Text is the fundamental view for presenting strings in the UI. It supports plain text, preset text styles, custom styling via `TextStyle`, and rich text with `AttributedString` segments.

The `content` property is reactive -- assigning a new value triggers an immediate UI update.

## Constructor

```python
nib.Text(
    content=None,
    strings=None,
    style=None,
    line_limit=None,
    truncation_mode=None,
    minimum_scale_factor=None,
    allows_tightening=False,
    text_case=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `str` | `None` | The text string to display. Provide either `content` or `strings`, not both. |
| `strings` | `list[AttributedString]` | `None` | A list of `AttributedString` objects for rich text with mixed styles. Provide either `content` or `strings`, not both. |
| `style` | `TextStyle` | `None` | A `TextStyle` that configures font, weight, color, and decorations. Can be a preset (`TextStyle.TITLE`, `TextStyle.BODY`) or a custom `TextStyle(...)` instance. |
| `line_limit` | `int` | `None` | Maximum number of lines to display. Text beyond this limit is truncated. |
| `truncation_mode` | `TruncationMode \| str` | `None` | How to truncate overflowing text. Options: `TruncationMode.HEAD`, `TruncationMode.MIDDLE`, `TruncationMode.TAIL`. |
| `minimum_scale_factor` | `float` | `None` | Minimum scale factor for text shrinking (0.0 to 1.0). When set, text shrinks to fit before truncating. |
| `allows_tightening` | `bool` | `False` | Whether to allow tightening inter-character spacing to fit text. |
| `text_case` | `TextCase \| str` | `None` | Text case transformation. Options: `TextCase.UPPERCASE`, `TextCase.LOWERCASE`. |
| `**modifiers` | | | Common view modifiers: `font`, `foreground_color`, `padding`, `background`, `opacity`, `width`, `height`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `content` | `str` | Get or set the displayed text. Setting triggers a UI update. |
| `strings` | `list[AttributedString]` | Get or set the attributed string segments. Setting clears `content` and triggers a UI update. |

## Examples

### Basic text display

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Text("Hello, World!"),
            nib.Text("Styled title", style=nib.TextStyle.TITLE),
            nib.Text("Body text", style=nib.TextStyle.BODY),
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Reactive counter

```python
import nib

def main(app: nib.App):
    counter = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.build(
        nib.VStack(controls=[
            counter,
            nib.Button("Increment", action=increment),
        ], spacing=12, padding=16)
    )

nib.run(main)
```

### Rich text with AttributedString

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Text(
            strings=[
                nib.AttributedString("Error: ", style=nib.TextStyle(
                    color="red", bold=True)),
                nib.AttributedString("File not found", style=nib.TextStyle.BODY),
            ],
            padding=16,
        )
    )

nib.run(main)
```
