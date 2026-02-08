# List

![List](../../../assets/img/controls/list.png)

A container that displays rows of data in a single scrollable column. List provides native list styling including row separators and is optimized for displaying collections of items.

Unlike a VStack inside a ScrollView, List offers a more native appearance suited for settings screens, menus, and data tables. It is commonly used together with `Section` for grouped content.

## Constructor

```python
nib.List(
    controls=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `controls` | `list[View]` | `None` | Child views displayed as rows. Can contain individual views or `Section` views for grouped content with headers and footers. |
| `**modifiers` | | | Common view modifiers: `padding`, `background`, `foreground_color`, `opacity`, `width`, `height`, etc. |

## Examples

### Simple item list

```python
import nib

def main(app: nib.App):
    app.build(
        nib.List(
            controls=[
                nib.Text("Apple"),
                nib.Text("Banana"),
                nib.Text("Cherry"),
                nib.Text("Date"),
            ],
            height=300,
        )
    )

nib.run(main)
```

### List with sections

Group related items with `Section` to add headers and footers.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.List(
            controls=[
                nib.Section(
                    controls=[nib.Text("Apple"), nib.Text("Banana")],
                    header="Fruits",
                ),
                nib.Section(
                    controls=[nib.Text("Carrot"), nib.Text("Broccoli")],
                    header="Vegetables",
                ),
            ],
            height=400,
        )
    )

nib.run(main)
```

### Settings-style list

Combine List, Section, and input controls to build a settings interface.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.List(
            controls=[
                nib.Section(
                    controls=[
                        nib.Toggle("Notifications", is_on=True),
                        nib.Toggle("Sound", is_on=False),
                    ],
                    header="Preferences",
                    footer="Manage your notification settings.",
                ),
                nib.Section(
                    controls=[
                        nib.NavigationLink("About", destination=[
                            nib.Text("About this app"),
                        ]),
                        nib.NavigationLink("Help", destination=[
                            nib.Text("Help page"),
                        ]),
                    ],
                    header="Information",
                ),
            ],
            height=400,
        )
    )

nib.run(main)
```
