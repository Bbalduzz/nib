# NavigationStack & NavigationLink

NavigationStack and NavigationLink work together to create hierarchical drill-down navigation interfaces. NavigationStack manages a stack of views, and NavigationLink creates tappable elements that push destination views onto the stack.

The stack maintains navigation history, allowing users to return to previous views. The root content is always at the bottom of the stack, with destination views pushed on top as the user navigates.

## Constructor

```python
nib.NavigationStack(
    controls=None,
    **modifiers,
)
```

```python
nib.NavigationLink(
    label=None,
    destination=None,
    **modifiers,
)
```

## Parameters

### NavigationStack

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Root content views displayed initially. These form the base of the navigation stack and are shown when no navigation has occurred or when the user navigates back to the root. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

### NavigationLink

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | required | The text label displayed for the navigation link. This text is shown as the tappable element. |
| `destination` | `list[View]` | `None` | Views to display when the link is tapped. These views are pushed onto the NavigationStack. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, etc. |

## Examples

### Basic navigation

```python
import nib

def main(app: nib.App):
    app.build(
        nib.NavigationStack(
            controls=[
                nib.List(
                    controls=[
                        nib.NavigationLink("Settings", destination=[
                            nib.VStack(
                                controls=[
                                    nib.Text("Settings", font=nib.Font.TITLE),
                                    nib.Toggle("Dark Mode", is_on=False),
                                    nib.Toggle("Notifications", is_on=True),
                                ],
                                spacing=12,
                                padding=16,
                            ),
                        ]),
                        nib.NavigationLink("About", destination=[
                            nib.Text("About this app", padding=16),
                        ]),
                    ],
                ),
            ],
            height=400,
        )
    )

nib.run(main)
```

### Settings navigation with sections

```python
import nib

def main(app: nib.App):
    app.build(
        nib.NavigationStack(
            controls=[
                nib.List(
                    controls=[
                        nib.Section(
                            controls=[
                                nib.NavigationLink("Profile", destination=[
                                    nib.VStack(
                                        controls=[
                                            nib.Text("Profile Settings", font=nib.Font.TITLE),
                                            nib.TextField(value="", placeholder="Display Name"),
                                        ],
                                        spacing=12,
                                        padding=16,
                                    ),
                                ]),
                                nib.NavigationLink("Notifications", destination=[
                                    nib.Form(controls=[
                                        nib.Toggle("Push", is_on=True),
                                        nib.Toggle("Email", is_on=False),
                                    ]),
                                ]),
                            ],
                            header="Account",
                        ),
                        nib.Section(
                            controls=[
                                nib.NavigationLink("Privacy", destination=[
                                    nib.Text("Privacy settings"),
                                ]),
                                nib.NavigationLink("Help", destination=[
                                    nib.Text("Help content"),
                                ]),
                            ],
                            header="General",
                        ),
                    ],
                ),
            ],
            height=500,
        )
    )

nib.run(main)
```

### Dynamic navigation links

Generate navigation links from a data source.

```python
import nib

def main(app: nib.App):
    pages = [
        {"title": "Dashboard", "content": "Dashboard overview"},
        {"title": "Analytics", "content": "Analytics data"},
        {"title": "Reports", "content": "Generated reports"},
    ]

    app.build(
        nib.NavigationStack(
            controls=[
                nib.List(
                    controls=[
                        nib.NavigationLink(
                            page["title"],
                            destination=[
                                nib.VStack(
                                    controls=[
                                        nib.Text(page["title"], font=nib.Font.TITLE),
                                        nib.Text(page["content"]),
                                    ],
                                    spacing=8,
                                    padding=16,
                                ),
                            ],
                        )
                        for page in pages
                    ],
                ),
            ],
            height=400,
        )
    )

nib.run(main)
```
