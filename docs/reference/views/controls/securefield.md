# SecureField

![SecureField control](../../../assets/img/controls/securefield.png)

A single-line text input that masks entered characters, suitable for passwords and other sensitive data. SecureField behaves like [TextField](textfield.md) but obscures the input so that characters are not visible on screen.

## Constructor

```python
nib.SecureField(
    placeholder="",
    value="",
    on_change=None,
    on_submit=None,
    style=None,
    disabled=False,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `placeholder` | `str` | `""` | Hint text displayed when the field is empty. |
| `value` | `str` | `""` | Initial text value (masked in the UI). Use the `value` property for reactive updates. |
| `on_change` | `Callable[[str], None]` | `None` | Callback called when text changes. Receives the new text value as a string argument. |
| `on_submit` | `Callable[[str], None]` | `None` | Callback called when the user presses Return/Enter. Receives the current text value. |
| `style` | `TextFieldStyle \| str` | `None` | Visual style. Options: `TextFieldStyle.automatic`, `TextFieldStyle.plain`, `TextFieldStyle.roundedBorder`. |
| `disabled` | `bool` | `False` | Whether the secure field is disabled and non-interactive. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `font`, `opacity`, `width`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `value` | `str` | Get or set the current text (masked in the UI). Setting triggers a UI update. |

## Examples

### Password input

```python
import nib

def main(app: nib.App):
    password_field = nib.SecureField(
        placeholder="Password",
        value="",
        style=nib.TextFieldStyle.roundedBorder,
    )

    app.build(
        nib.VStack(controls=[
            nib.Text("Password:"),
            password_field,
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Login form with submit

```python
import nib

def main(app: nib.App):
    username = nib.TextField(
        placeholder="Username",
        value="",
        style=nib.TextFieldStyle.roundedBorder,
    )
    password = nib.SecureField(
        placeholder="Password",
        value="",
        style=nib.TextFieldStyle.roundedBorder,
    )
    status = nib.Text("")

    def login():
        if username.value and password.value:
            status.content = "Logging in..."
        else:
            status.content = "Please fill in all fields"

    app.build(
        nib.VStack(controls=[
            nib.Text("Sign In", style=nib.TextStyle.TITLE),
            username,
            password,
            nib.Button("Log In", action=login,
                        style=nib.ButtonStyle.borderedProminent),
            status,
        ], spacing=12, padding=20, width=280)
    )

nib.run(main)
```

### Secure field with validation

```python
import nib

def main(app: nib.App):
    hint = nib.Text("", foreground_color=nib.Color.RED, font=nib.Font.CAPTION)

    def validate(text: str):
        if len(text) < 8:
            hint.content = "Password must be at least 8 characters"
        else:
            hint.content = ""

    app.build(
        nib.VStack(controls=[
            nib.SecureField(
                placeholder="Enter a strong password",
                value="",
                on_change=validate,
                style=nib.TextFieldStyle.roundedBorder,
            ),
            hint,
        ], spacing=4, padding=16)
    )

nib.run(main)
```
