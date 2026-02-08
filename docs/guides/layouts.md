# Building Layouts

Nib provides a set of layout containers that mirror SwiftUI's layout system. Every container takes a `controls` list of child views and arranges them according to its rules.

---

## VStack -- Vertical Stacking

`VStack` arranges children from top to bottom. Use `spacing` to control the gap between children and `alignment` to control horizontal positioning.

```python
import nib

nib.VStack(
    controls=[
        nib.Text("First"),
        nib.Text("Second"),
        nib.Text("Third"),
    ],
    spacing=8,
    alignment=nib.HorizontalAlignment.CENTER,
)
```

Alignment options for VStack:

| Value | Effect |
|-------|--------|
| `HorizontalAlignment.LEADING` | Align children to the left |
| `HorizontalAlignment.CENTER` | Center children (default) |
| `HorizontalAlignment.TRAILING` | Align children to the right |

A left-aligned card:

```python
nib.VStack(
    controls=[
        nib.Text("Account", font=nib.Font.HEADLINE),
        nib.Text("user@example.com", foreground_color=nib.Color.SECONDARY),
    ],
    spacing=4,
    alignment=nib.HorizontalAlignment.LEADING,
    padding=16,
)
```

---

## HStack -- Horizontal Stacking

`HStack` arranges children from left to right. Use `alignment` to control vertical positioning within the row.

```python
nib.HStack(
    controls=[
        nib.SFSymbol("star.fill", foreground_color=nib.Color.YELLOW),
        nib.Text("Favorites"),
    ],
    spacing=8,
    alignment=nib.VerticalAlignment.CENTER,
)
```

Alignment options for HStack:

| Value | Effect |
|-------|--------|
| `VerticalAlignment.TOP` | Align children to the top |
| `VerticalAlignment.CENTER` | Center children vertically (default) |
| `VerticalAlignment.BOTTOM` | Align children to the bottom |

A toolbar-style row with a centered title:

```python
nib.HStack(
    controls=[
        nib.Button("Back", action=go_back),
        nib.Spacer(),
        nib.Text("Title", font=nib.Font.HEADLINE),
        nib.Spacer(),
        nib.Button("Done", action=finish),
    ],
    spacing=8,
    padding={"horizontal": 16, "vertical": 8},
)
```

---

## ZStack -- Overlays

`ZStack` layers children on top of each other. The first child is at the back, and each subsequent child is drawn on top. Use `alignment` to position children within the stack.

```python
nib.ZStack(
    controls=[
        nib.Rectangle(corner_radius=12, fill=nib.Color.BLUE),
        nib.Text("Overlay Text", foreground_color=nib.Color.WHITE),
    ],
    alignment=nib.Alignment.CENTER,
)
```

Alignment options for ZStack:

| Value | Position |
|-------|----------|
| `Alignment.TOP_LEADING` | Top-left corner |
| `Alignment.TOP` | Top center |
| `Alignment.TOP_TRAILING` | Top-right corner |
| `Alignment.LEADING` | Center-left |
| `Alignment.CENTER` | Dead center (default) |
| `Alignment.TRAILING` | Center-right |
| `Alignment.BOTTOM_LEADING` | Bottom-left corner |
| `Alignment.BOTTOM` | Bottom center |
| `Alignment.BOTTOM_TRAILING` | Bottom-right corner |

A notification badge over an icon:

```python
nib.ZStack(
    controls=[
        nib.SFSymbol("bell.fill", font=nib.Font.TITLE),
        nib.Text(
            "3",
            font=nib.Font.CAPTION,
            foreground_color=nib.Color.WHITE,
            background=nib.Circle(fill=nib.Color.RED),
            padding=4,
        ),
    ],
    alignment=nib.Alignment.TOP_TRAILING,
)
```

---

## Nesting Stacks

Combine stacks to build complex layouts. This is the primary way to compose UI in Nib.

```python
import nib

def main(app: nib.App):
    app.title = "Contacts"
    app.icon = nib.SFSymbol("person.2")
    app.width = 300
    app.height = 400

    app.build(
        nib.VStack(
            controls=[
                # Header row
                nib.HStack(
                    controls=[
                        nib.Text("Contacts", font=nib.Font.TITLE),
                        nib.Spacer(),
                        nib.Button("Add", action=lambda: None),
                    ],
                    padding={"horizontal": 16, "top": 16},
                ),

                # Contact cards
                nib.VStack(
                    controls=[
                        _contact_row("Alice", "alice@example.com"),
                        _contact_row("Bob", "bob@example.com"),
                        _contact_row("Charlie", "charlie@example.com"),
                    ],
                    spacing=8,
                    padding=16,
                ),
            ],
        )
    )

def _contact_row(name, email):
    return nib.HStack(
        controls=[
            nib.SFSymbol("person.circle.fill", foreground_color=nib.Color.BLUE),
            nib.VStack(
                controls=[
                    nib.Text(name, font=nib.Font.HEADLINE),
                    nib.Text(email, font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY),
                ],
                alignment=nib.HorizontalAlignment.LEADING,
                spacing=2,
            ),
        ],
        spacing=10,
        alignment=nib.VerticalAlignment.CENTER,
    )

nib.run(main)
```

---

## ScrollView

`ScrollView` wraps content in a scrollable region. Set the `axes` parameter to control direction.

```python
nib.ScrollView(
    controls=[
        nib.VStack(
            controls=[nib.Text(f"Item {i}") for i in range(50)],
            spacing=4,
        ),
    ],
    axes="vertical",  # "vertical" (default), "horizontal", or "both"
    shows_indicators=True,
    height=300,
)
```

A horizontal image gallery:

```python
nib.ScrollView(
    controls=[
        nib.HStack(
            controls=[
                nib.Rectangle(corner_radius=8, fill=nib.Color.BLUE, width=120, height=80),
                nib.Rectangle(corner_radius=8, fill=nib.Color.GREEN, width=120, height=80),
                nib.Rectangle(corner_radius=8, fill=nib.Color.ORANGE, width=120, height=80),
                nib.Rectangle(corner_radius=8, fill=nib.Color.PURPLE, width=120, height=80),
            ],
            spacing=8,
        ),
    ],
    axes="horizontal",
    shows_indicators=False,
)
```

!!! tip
    Wrap your scroll content inside a single VStack or HStack. ScrollView determines its scrollable area from the combined size of its children.

---

## List

`List` displays rows in a native scrollable column with platform-standard styling (row separators, insets). Use it for settings screens, data tables, and any list-based UI.

```python
nib.List(
    controls=[
        nib.Text("Apple"),
        nib.Text("Banana"),
        nib.Text("Cherry"),
    ],
)
```

Each child is rendered as a separate row. You can use any view as a row:

```python
nib.List(
    controls=[
        nib.HStack(
            controls=[
                nib.SFSymbol("person.circle"),
                nib.Text("Alice"),
                nib.Spacer(),
                nib.Text("Online", foreground_color=nib.Color.GREEN),
            ],
            spacing=8,
        ),
        nib.HStack(
            controls=[
                nib.SFSymbol("person.circle"),
                nib.Text("Bob"),
                nib.Spacer(),
                nib.Text("Offline", foreground_color=nib.Color.GRAY),
            ],
            spacing=8,
        ),
    ],
    height=200,
)
```

---

## Section

`Section` groups content within a `List` or `Form`, providing optional header and footer text.

```python
nib.List(
    controls=[
        nib.Section(
            controls=[
                nib.Text("Apple"),
                nib.Text("Banana"),
            ],
            header="Fruits",
        ),
        nib.Section(
            controls=[
                nib.Text("Carrot"),
                nib.Text("Broccoli"),
            ],
            header="Vegetables",
            footer="Eat your greens!",
        ),
    ],
)
```

!!! note
    Section is designed for use inside List or Form. Outside these containers, it may not render with the expected visual grouping.

---

## Form

`Form` is a container for data-entry controls. On macOS it defaults to a two-column layout with labels on the left and controls on the right.

```python
nib.Form(
    controls=[
        nib.Toggle("Dark Mode", is_on=False),
        nib.Picker("Language", selection="English", options=["English", "Spanish", "French"]),
        nib.TextField(value="", placeholder="Username"),
    ],
    style=nib.FormStyle.COLUMNS,
)
```

Form styles:

| Style | Effect |
|-------|--------|
| `FormStyle.AUTOMATIC` | Platform default |
| `FormStyle.COLUMNS` | Two-column label/control layout (macOS default) |
| `FormStyle.GROUPED` | Grouped sections with visual separation |

A settings form with sections:

```python
nib.Form(
    controls=[
        nib.Section(
            controls=[
                nib.Toggle("Push Notifications", is_on=True),
                nib.Toggle("Email Notifications", is_on=False),
            ],
            header="Notifications",
            footer="Choose how you want to be notified.",
        ),
        nib.Section(
            controls=[
                nib.Picker("Theme", selection="System", options=["Light", "Dark", "System"]),
                nib.Slider("Font Size", value=14, min_value=10, max_value=24),
            ],
            header="Appearance",
        ),
    ],
    style=nib.FormStyle.GROUPED,
)
```

---

## Spacer

`Spacer` is a flexible view that expands to fill available space in a stack. It is one of the most useful layout primitives.

```python
# Push "Right" to the trailing edge
nib.HStack(
    controls=[
        nib.Text("Left"),
        nib.Spacer(),
        nib.Text("Right"),
    ],
)
```

Use `min_length` to guarantee a minimum gap:

```python
nib.HStack(
    controls=[
        nib.Text("A"),
        nib.Spacer(min_length=20),
        nib.Text("B"),
        nib.Spacer(min_length=20),
        nib.Text("C"),
    ],
)
```

In a VStack, Spacer expands vertically. This pushes content to the top and bottom:

```python
nib.VStack(
    controls=[
        nib.Text("Header", font=nib.Font.HEADLINE),
        nib.Spacer(),
        nib.Text("Footer", font=nib.Font.CAPTION),
    ],
    height=400,
)
```

---

## Divider

`Divider` draws a thin horizontal (in VStack) or vertical (in HStack) line to visually separate content.

```python
nib.VStack(
    controls=[
        nib.Text("Section 1"),
        nib.Divider(),
        nib.Text("Section 2"),
    ],
    spacing=8,
)
```

---

## Grid and GridRow

`Grid` arranges views in a fixed two-dimensional grid with explicit rows. Each `GridRow` defines one row of cells.

```python
nib.Grid(
    controls=[
        nib.GridRow(controls=[nib.Text("Name"), nib.Text("Score")]),
        nib.GridRow(controls=[nib.Text("Alice"), nib.Text("95")]),
        nib.GridRow(controls=[nib.Text("Bob"), nib.Text("87")]),
    ],
    horizontal_spacing=20,
    vertical_spacing=8,
)
```

!!! info
    Grid sizes all its children eagerly. For large data sets, use LazyVGrid or LazyHGrid instead.

---

## LazyVGrid

`LazyVGrid` creates a vertically-scrolling grid. You define the column layout with `GridItem` specifications, and Nib fills columns left to right, wrapping into new rows.

```python
from nib import GridItem, GridItemSize

nib.LazyVGrid(
    columns=[
        GridItem(GridItemSize.FLEXIBLE),
        GridItem(GridItemSize.FLEXIBLE),
        GridItem(GridItemSize.FLEXIBLE),
    ],
    controls=[
        nib.Rectangle(corner_radius=8, fill=nib.Color.BLUE, height=60)
        for _ in range(9)
    ],
    spacing=10,
)
```

### GridItem sizing strategies

| Strategy | Constructor | Behavior |
|----------|-------------|----------|
| Fixed | `GridItem(GridItemSize.FIXED, 100)` | Exactly 100 points wide |
| Flexible | `GridItem(GridItemSize.FLEXIBLE, 50)` | At least 50pt, expands to fill |
| Adaptive | `GridItem(GridItemSize.ADAPTIVE, 80)` | Fits as many 80pt+ columns as possible |

Convenience constructors are also available:

```python
from nib import fixed, flexible, adaptive

# Three fixed 100pt columns
nib.LazyVGrid(columns=[fixed(100), fixed(100), fixed(100)], controls=[...])

# As many columns as fit, each at least 80pt
nib.LazyVGrid(columns=[adaptive(80)], controls=[...])

# Two flexible columns, minimum 50pt each
nib.LazyVGrid(columns=[flexible(50), flexible(50)], controls=[...])
```

---

## LazyHGrid

`LazyHGrid` is the horizontal counterpart: you define rows and children flow horizontally, wrapping into new columns.

```python
nib.ScrollView(
    controls=[
        nib.LazyHGrid(
            rows=[
                GridItem(GridItemSize.FIXED, 50),
                GridItem(GridItemSize.FIXED, 50),
            ],
            controls=[
                nib.Rectangle(corner_radius=4, fill=nib.Color.GREEN, width=80)
                for _ in range(12)
            ],
            spacing=10,
        ),
    ],
    axes="horizontal",
)
```

!!! tip
    Wrap a LazyHGrid in a horizontal ScrollView so the content can scroll when it exceeds the visible width.

---

## Full Example

A complete app demonstrating multiple layout techniques:

```python
import nib

def main(app: nib.App):
    app.title = "Layout Demo"
    app.icon = nib.SFSymbol("rectangle.3.group")
    app.width = 320
    app.height = 480

    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        # Header
                        nib.HStack(
                            controls=[
                                nib.Text("Dashboard", font=nib.Font.TITLE),
                                nib.Spacer(),
                                nib.SFSymbol("gear", foreground_color=nib.Color.SECONDARY),
                            ],
                        ),

                        nib.Divider(),

                        # Stats grid
                        nib.LazyVGrid(
                            columns=[nib.GridItem(nib.GridItemSize.FLEXIBLE), nib.GridItem(nib.GridItemSize.FLEXIBLE)],
                            controls=[
                                _stat_card("Downloads", "1,234", nib.Color.BLUE),
                                _stat_card("Users", "567", nib.Color.GREEN),
                                _stat_card("Revenue", "$8.9k", nib.Color.ORANGE),
                                _stat_card("Rating", "4.8", nib.Color.PURPLE),
                            ],
                            spacing=8,
                        ),

                        # Recent items
                        nib.List(
                            controls=[
                                nib.Section(
                                    controls=[
                                        nib.Text("v2.1 released"),
                                        nib.Text("Bug fix deployed"),
                                        nib.Text("New feature added"),
                                    ],
                                    header="Recent Activity",
                                ),
                            ],
                            height=200,
                        ),
                    ],
                    spacing=12,
                    padding=16,
                ),
            ],
        )
    )

def _stat_card(title, value, color):
    return nib.VStack(
        controls=[
            nib.Text(value, font=nib.Font.TITLE, foreground_color=color),
            nib.Text(title, font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY),
        ],
        spacing=4,
        padding=12,
        background=nib.Rectangle(corner_radius=8, fill=nib.Color(hex="#1a1a1a")),
    )

nib.run(main)
```
