# TextField

![TextField control](../../../assets/img/controls/textfield.png)

A single-line text input control with placeholder text, change callbacks, and submit handling. The `value` property is reactive -- reading and writing it directly allows for straightforward state management.

## Constructor

```python
nib.TextField(
    placeholder="",
    value="",
    on_change=None,
    on_submit=None,
    style=None,
    autocapitalization=None,
    autocorrection=None,
    keyboard_type=None,
    submit_label=None,
    disabled=False,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `placeholder` | `str` | `""` | Hint text displayed when the field is empty. |
| `value` | `str` | `""` | Initial text value. Use the `value` property for reactive updates. |
| `on_change` | `Callable[[str], None]` | `None` | Callback called when text changes. Receives the new text as a string argument. |
| `on_submit` | `Callable[[str], None]` | `None` | Callback called when the user presses Return/Enter. Receives the current text value. |
| `style` | `TextFieldStyle \| str` | `None` | Visual style. Options: `TextFieldStyle.automatic`, `TextFieldStyle.plain`, `TextFieldStyle.roundedBorder`. |
| `autocapitalization` | `str` | `None` | Autocapitalization behavior. Options: `"none"`, `"words"`, `"sentences"`, `"allCharacters"`. |
| `autocorrection` | `bool` | `None` | Whether to enable autocorrection. `True` to enable, `False` to disable, `None` for system default. |
| `keyboard_type` | `str` | `None` | Keyboard type. Options: `"default"`, `"asciiCapable"`, `"numbersAndPunctuation"`, `"URL"`, `"numberPad"`, `"emailAddress"`, `"decimalPad"`. |
| `submit_label` | `str` | `None` | Label for the Return/Enter key (e.g., `"Search"`, `"Go"`). |
| `disabled` | `bool` | `False` | Whether the text field is disabled and non-interactive. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `font`, `opacity`, `width`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `str` | Get or set the current text. Setting triggers a UI update. |

## Examples

### Basic text input with placeholder

```python
import nib

def main(app: nib.App):
    name_field = nib.TextField(
        placeholder="Enter your name",
        value="",
        style=nib.TextFieldStyle.roundedBorder,
    )

    app.build(
        nib.VStack(controls=[
            nib.Text("Name:"),
            name_field,
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Search field with submit

```python
import nib

def main(app: nib.App):
    results = nib.Text("")

    def search(query: str):
        results.content = f"Searching for: {query}"

    app.build(
        nib.VStack(controls=[
            nib.TextField(
                placeholder="Search...",
                value="",
                on_submit=search,
                submit_label="Search",
                style=nib.TextFieldStyle.roundedBorder,
                width=250,
            ),
            results,
        ], spacing=12, padding=16)
    )

nib.run(main)
```

### Reactive value updates

```python
import nib

def main(app: nib.App):
    display = nib.Text("Characters: 0")
    input_field = nib.TextField(
        placeholder="Type something...",
        value="",
        on_change=lambda text: setattr(
            display, "content", f"Characters: {len(text)}"
        ),
        style=nib.TextFieldStyle.roundedBorder,
    )

    app.build(
        nib.VStack(controls=[input_field, display], spacing=8, padding=16)
    )

nib.run(main)
```
