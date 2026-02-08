# TextEditor

![TextEditor control](../../../assets/img/controls/texteditor.png)

A multi-line text editing view, similar to an HTML `<textarea>`. TextEditor is suited for editing longer content such as notes, descriptions, or code. The `text` property is reactive -- assigning a new value triggers an immediate UI update.

## Constructor

```python
nib.TextEditor(
    text="",
    placeholder=None,
    on_change=None,
    style=None,
    font=None,
    foreground_color=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | `""` | Initial text content. |
| `placeholder` | `str` | `None` | Placeholder text displayed when the editor is empty (macOS 14+). |
| `on_change` | `Callable[[str], None]` | `None` | Callback called when text changes. Receives the new text as a string argument. |
| `style` | `TextEditorStyle` | `None` | Comprehensive style configuration including font, colors, line spacing, alignment, and editor appearance. |
| `font` | `Font` | `None` | Text font. Overridden by `style.font` if both are provided. |
| `foreground_color` | `Color \| str` | `None` | Text color. Overridden by `style.foreground_color` if both are provided. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `opacity`, `width`, `height`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `text` | `str` | Get or set the editor text content. Setting triggers a UI update. |
| `placeholder` | `str` | Get or set the placeholder text. Setting triggers a UI update. |
| `style` | `TextEditorStyle` | Get or set the style configuration. Setting triggers a UI update. |

## Examples

### Simple note editor

```python
import nib

def main(app: nib.App):
    editor = nib.TextEditor(
        text="",
        placeholder="Write your notes here...",
        width=300,
        height=200,
    )

    app.build(
        nib.VStack(controls=[
            nib.Text("Notes", style=nib.TextStyle.TITLE),
            editor,
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Editor with change tracking

```python
import nib

def main(app: nib.App):
    char_count = nib.Text("0 characters")

    def on_text_change(text: str):
        char_count.content = f"{len(text)} characters"

    app.build(
        nib.VStack(controls=[
            nib.TextEditor(
                text="",
                placeholder="Start typing...",
                on_change=on_text_change,
                width=300,
                height=150,
            ),
            char_count,
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Styled code editor

```python
import nib

def main(app: nib.App):
    app.build(
        nib.TextEditor(
            text='print("Hello, World!")',
            style=nib.TextEditorStyle(
                font=nib.Font.custom("Menlo", size=13),
                foreground_color=nib.Color.PRIMARY,
                background_color=nib.Color(hex="#1E1E1E"),
                line_spacing=6,
                editor_style=nib.EditorStyle.PLAIN,
            ),
            width=400,
            height=250,
            padding=16,
        )
    )

nib.run(main)
```
