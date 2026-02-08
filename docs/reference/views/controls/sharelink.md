# ShareLink

![ShareLink control](../../../assets/img/controls/sharelink.png)

A button that presents the native macOS share sheet, allowing users to share text, URLs, or files through system sharing services. The share sheet displays available targets such as AirDrop, Mail, Messages, and third-party apps.

## Constructor

```python
nib.ShareLink(
    items,
    content=None,
    label=None,
    icon=None,
    subject=None,
    message=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `list[str]` | *(required)* | Items to share. Can be strings (plain text), URLs, or file paths. |
| `content` | `View` | `None` | Custom view to use as the button label. Overrides `label` and `icon`. |
| `label` | `str` | `None` | Button label text. Used when `content` is not provided. |
| `icon` | `str` | `None` | SF Symbol name for the button icon. Used alongside `label` when `content` is not provided. |
| `subject` | `str` | `None` | Subject line for email shares. |
| `message` | `str` | `None` | Pre-filled message body for social shares. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `items` | `list[str]` | Get or set the items to share. |
| `content` | `View` | Get or set the custom button view. |
| `label` | `str` | Get or set the button label text. |
| `icon` | `str` | Get or set the SF Symbol icon name. |

## Examples

### Share text with label

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ShareLink(
            items=["Check out this cool app!"],
            label="Share",
            icon="square.and.arrow.up",
            padding=16,
        )
    )

nib.run(main)
```

### Share a URL with custom content

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ShareLink(
            items=["https://example.com"],
            content=nib.HStack(controls=[
                nib.Image(system_name="square.and.arrow.up"),
                nib.Text("Share Link"),
            ], spacing=4),
            subject="Check this out",
            padding=16,
        )
    )

nib.run(main)
```

### Share a file

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(controls=[
            nib.Text("Export", style=nib.TextStyle.TITLE),
            nib.ShareLink(
                items=["/path/to/report.pdf"],
                label="Share Report",
                icon="doc.fill",
            ),
        ], spacing=12, padding=16)
    )

nib.run(main)
```
