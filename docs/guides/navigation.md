# Navigation

Nib provides SwiftUI-style navigation components for building hierarchical, drill-down interfaces. Use `NavigationStack` as the container, `NavigationLink` for push navigation, and `DisclosureGroup` for collapsible sections.

## NavigationStack

`NavigationStack` is a container that manages a stack of views. It provides the context needed for `NavigationLink` to push destination views:

```python
import nib

nib.NavigationStack(
    controls=[
        nib.Text("Root View"),
        nib.NavigationLink("Go to Details", destination=[
            nib.Text("Detail View"),
        ]),
    ],
)
```

When a user taps a `NavigationLink`, the destination views replace the current content with an animated transition. A back button appears automatically to return to the previous view.

| Parameter | Type | Description |
|-----------|------|-------------|
| `controls` | `list[View]` | Root content views displayed initially |

Standard view modifiers are also supported.

## NavigationLink

`NavigationLink` creates a tappable row that navigates to a destination view when tapped. It automatically displays a disclosure chevron:

```python
nib.NavigationLink(
    label="Profile Settings",
    destination=[
        nib.VStack(
            controls=[
                nib.Text("Profile", font=nib.Font.TITLE),
                nib.TextField(value="", placeholder="Display Name"),
                nib.Toggle("Show Online Status", is_on=True),
            ],
            spacing=12,
            padding=16,
        ),
    ],
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | `str` | Text displayed as the tappable element |
| `destination` | `list[View]` | Views to display when navigated to |

!!! note
    `NavigationLink` must be placed inside a `NavigationStack` for navigation to work. Without the surrounding stack, tapping the link has no effect.

## Building a settings-style navigation

The most common pattern is a `NavigationStack` containing a `List` of `NavigationLink` elements, similar to the macOS System Settings app:

```python
import nib


def main(app: nib.App):
    app.title = "Preferences"
    app.icon = nib.SFSymbol("gear")
    app.width = 350
    app.height = 400

    app.build(
        nib.NavigationStack(
            controls=[
                nib.List(
                    controls=[
                        nib.Section(
                            header="Account",
                            controls=[
                                nib.NavigationLink(
                                    label="Profile",
                                    destination=[
                                        nib.VStack(
                                            controls=[
                                                nib.Text("Profile", font=nib.Font.TITLE),
                                                nib.TextField(
                                                    value="",
                                                    placeholder="Username",
                                                ),
                                                nib.TextField(
                                                    value="",
                                                    placeholder="Email",
                                                ),
                                            ],
                                            spacing=12,
                                            padding=16,
                                        ),
                                    ],
                                ),
                                nib.NavigationLink(
                                    label="Security",
                                    destination=[
                                        nib.VStack(
                                            controls=[
                                                nib.Text("Security", font=nib.Font.TITLE),
                                                nib.Toggle("Two-Factor Auth", is_on=False),
                                                nib.Toggle("Biometric Login", is_on=True),
                                            ],
                                            spacing=12,
                                            padding=16,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        nib.Section(
                            header="Appearance",
                            controls=[
                                nib.NavigationLink(
                                    label="Theme",
                                    destination=[
                                        nib.VStack(
                                            controls=[
                                                nib.Text("Theme", font=nib.Font.TITLE),
                                                nib.Picker(
                                                    items=["System", "Light", "Dark"],
                                                    selected="System",
                                                ),
                                                nib.Slider(
                                                    value=14,
                                                    min_value=10,
                                                    max_value=24,
                                                    label="Font Size",
                                                ),
                                            ],
                                            spacing=12,
                                            padding=16,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    )


nib.run(main)
```

## DisclosureGroup

`DisclosureGroup` creates a collapsible section that the user can expand or collapse by clicking the header. This is useful for progressive disclosure of optional or advanced content:

```python
nib.DisclosureGroup(
    label="Advanced Options",
    controls=[
        nib.Toggle("Enable Logging", is_on=False),
        nib.Toggle("Developer Mode", is_on=False),
        nib.Slider(value=50, min_value=0, max_value=100, label="Cache Size"),
    ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | -- | Text label for the header |
| `controls` | `list[View]` | `[]` | Child views shown when expanded |
| `is_expanded` | `bool` | `False` | Initial expansion state |
| `on_expand` | `Callable[[bool], None]` | `None` | Callback when state changes |

### Initially expanded

```python
nib.DisclosureGroup(
    label="Quick Settings",
    controls=[
        nib.Toggle("Wi-Fi", is_on=True),
        nib.Toggle("Bluetooth", is_on=True),
    ],
    is_expanded=True,
)
```

### Tracking expansion state

```python
def on_expand(expanded: bool):
    print(f"Section is now {'open' if expanded else 'closed'}")

nib.DisclosureGroup(
    label="Details",
    controls=[nib.Text("Hidden content")],
    on_expand=on_expand,
)
```

## Combining navigation and disclosure

You can nest `DisclosureGroup` inside a `NavigationStack` to create interfaces with both drill-down navigation and collapsible sections:

```python
import nib


def main(app: nib.App):
    app.title = "Config"
    app.icon = nib.SFSymbol("slider.horizontal.3")
    app.width = 350
    app.height = 450

    app.build(
        nib.NavigationStack(
            controls=[
                nib.ScrollView(
                    controls=[
                        nib.VStack(
                            controls=[
                                nib.NavigationLink(
                                    label="Network",
                                    destination=[
                                        nib.VStack(
                                            controls=[
                                                nib.Text("Network", font=nib.Font.TITLE),
                                                nib.Toggle("Auto Connect", is_on=True),
                                                nib.DisclosureGroup(
                                                    label="Proxy Settings",
                                                    controls=[
                                                        nib.TextField(
                                                            value="",
                                                            placeholder="Host",
                                                        ),
                                                        nib.TextField(
                                                            value="",
                                                            placeholder="Port",
                                                        ),
                                                    ],
                                                ),
                                                nib.DisclosureGroup(
                                                    label="DNS Settings",
                                                    controls=[
                                                        nib.TextField(
                                                            value="",
                                                            placeholder="Primary DNS",
                                                        ),
                                                        nib.TextField(
                                                            value="",
                                                            placeholder="Secondary DNS",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                            spacing=12,
                                            padding=16,
                                        ),
                                    ],
                                ),
                                nib.NavigationLink(
                                    label="Storage",
                                    destination=[
                                        nib.VStack(
                                            controls=[
                                                nib.Text("Storage", font=nib.Font.TITLE),
                                                nib.ProgressView(
                                                    value=0.65,
                                                    label="Disk Usage",
                                                ),
                                                nib.Button("Clear Cache"),
                                            ],
                                            spacing=12,
                                            padding=16,
                                        ),
                                    ],
                                ),
                            ],
                            spacing=4,
                            padding=8,
                        ),
                    ],
                ),
            ],
        )
    )


nib.run(main)
```

!!! tip
    `DisclosureGroup` is a good alternative to `NavigationLink` when the content is short and does not warrant a full screen transition. Use navigation for complex sub-pages and disclosure groups for inline expandable sections.
