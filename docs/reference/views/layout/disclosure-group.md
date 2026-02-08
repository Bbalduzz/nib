# DisclosureGroup

![DisclosureGroup](../../../assets/img/controls/disclosure_group.png)

A collapsible container that shows or hides content on demand. DisclosureGroup displays a label with a disclosure indicator (chevron) that users can tap to reveal or hide the contained content.

This is useful for organizing optional or advanced settings, creating accordion-style interfaces, or reducing visual clutter by hiding less frequently used options.

## Constructor

```python
nib.DisclosureGroup(
    label=None,
    controls=None,
    is_expanded=False,
    on_expand=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | required | The text label displayed in the header. This text is always visible regardless of the expansion state. |
| `controls` | `list[View]` | `None` | Child views shown when the group is expanded and hidden when collapsed. |
| `is_expanded` | `bool` | `False` | Initial expansion state. `True` starts expanded with content visible; `False` starts collapsed. |
| `on_expand` | `Callable[[bool], None]` | `None` | Callback invoked when the expansion state changes. Receives `True` when expanded, `False` when collapsed. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Examples

### Advanced options

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Toggle("Basic setting", is_on=True),
                nib.DisclosureGroup(
                    "Advanced Options",
                    controls=[
                        nib.Toggle("Enable logging", is_on=False),
                        nib.Toggle("Developer mode", is_on=False),
                        nib.Slider("Verbosity", value=50, min_value=0, max_value=100),
                    ],
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### Initially expanded group

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.DisclosureGroup(
                    "Quick Settings",
                    controls=[
                        nib.Toggle("Wi-Fi", is_on=True),
                        nib.Toggle("Bluetooth", is_on=True),
                        nib.Toggle("AirDrop", is_on=False),
                    ],
                    is_expanded=True,
                ),
                nib.DisclosureGroup(
                    "Network Details",
                    controls=[
                        nib.Text("IP: 192.168.1.100"),
                        nib.Text("DNS: 8.8.8.8"),
                    ],
                    is_expanded=False,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

### With expansion callback

Track when users expand or collapse sections.

```python
import nib

def main(app: nib.App):
    status = nib.Text("Sections collapsed")

    def on_details_expand(expanded):
        if expanded:
            status.content = "Details section opened"
        else:
            status.content = "Details section closed"

    app.build(
        nib.VStack(
            controls=[
                status,
                nib.DisclosureGroup(
                    "Details",
                    controls=[
                        nib.Text("Name: Nib Framework"),
                        nib.Text("Version: 1.0.0"),
                        nib.Text("Platform: macOS"),
                    ],
                    on_expand=on_details_expand,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```
