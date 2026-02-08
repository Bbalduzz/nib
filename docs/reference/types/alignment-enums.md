# Alignment Enums

Nib provides alignment enums that control how views are positioned within their containers. Each enum maps directly to a SwiftUI alignment type.

---

## HorizontalAlignment

Controls horizontal alignment of children within a `VStack`.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `HorizontalAlignment.LEADING` | `.leading` | Align children to the left (LTR) or right (RTL) edge. |
| `HorizontalAlignment.CENTER` | `.center` | Center children horizontally (default). |
| `HorizontalAlignment.TRAILING` | `.trailing` | Align children to the right (LTR) or left (RTL) edge. |

```python
import nib

nib.VStack(
    controls=[
        nib.Text("Left-aligned title"),
        nib.Text("Left-aligned body"),
    ],
    alignment=nib.HorizontalAlignment.LEADING,
    spacing=4,
)
```

---

## VerticalAlignment

Controls vertical alignment of children within an `HStack`.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `VerticalAlignment.TOP` | `.top` | Align children to the top edge. |
| `VerticalAlignment.CENTER` | `.center` | Center children vertically (default). |
| `VerticalAlignment.BOTTOM` | `.bottom` | Align children to the bottom edge. |

```python
import nib

nib.HStack(
    controls=[
        nib.Text("Label", font=nib.Font.CAPTION),
        nib.Text("Value", font=nib.Font.TITLE),
    ],
    alignment=nib.VerticalAlignment.BOTTOM,
    spacing=8,
)
```

---

## Alignment

Combined two-dimensional alignment for `ZStack` and the `frame` modifier. Specifies both horizontal and vertical alignment simultaneously.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `Alignment.TOP_LEADING` | `.topLeading` | Top-left corner. |
| `Alignment.TOP` | `.top` | Top edge, centered horizontally. |
| `Alignment.TOP_TRAILING` | `.topTrailing` | Top-right corner. |
| `Alignment.LEADING` | `.leading` | Left edge, centered vertically. |
| `Alignment.CENTER` | `.center` | Center of the view (default). |
| `Alignment.TRAILING` | `.trailing` | Right edge, centered vertically. |
| `Alignment.BOTTOM_LEADING` | `.bottomLeading` | Bottom-left corner. |
| `Alignment.BOTTOM` | `.bottom` | Bottom edge, centered horizontally. |
| `Alignment.BOTTOM_TRAILING` | `.bottomTrailing` | Bottom-right corner. |

```python
import nib

# Badge in the top-right corner of a ZStack
nib.ZStack(
    controls=[
        nib.Rectangle(fill="#333", width=200, height=100, corner_radius=12),
        nib.Text(
            "3",
            font=nib.Font.CAPTION,
            foreground_color=nib.Color.WHITE,
            background=nib.Color.RED,
            padding={"horizontal": 6, "vertical": 2},
            corner_radius=8,
        ),
    ],
    alignment=nib.Alignment.TOP_TRAILING,
)
```

---

## ScrollAxis

Controls the scroll direction for `ScrollView` containers.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ScrollAxis.VERTICAL` | `.vertical` | Scroll vertically (default). |
| `ScrollAxis.HORIZONTAL` | `.horizontal` | Scroll horizontally. |
| `ScrollAxis.BOTH` | `[.vertical, .horizontal]` | Scroll in both directions. |

```python
import nib

# Vertical scrolling list
nib.ScrollView(
    controls=[nib.Text(f"Item {i}") for i in range(50)],
    axis=nib.ScrollAxis.VERTICAL,
)

# Horizontal scrolling row
nib.ScrollView(
    controls=[
        nib.Rectangle(fill="blue", width=100, height=100, corner_radius=8)
        for _ in range(10)
    ],
    axis=nib.ScrollAxis.HORIZONTAL,
)
```

## Examples

### Combining alignments in a layout

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Header aligned to leading edge
                nib.Text("My App", font=nib.Font.LARGE_TITLE),

                # Content in a ZStack with alignment
                nib.ZStack(
                    controls=[
                        nib.Rectangle(
                            fill="#1E1E1E",
                            width=250,
                            height=150,
                            corner_radius=12,
                        ),
                        nib.Text(
                            "Centered",
                            foreground_color=nib.Color.WHITE,
                        ),
                    ],
                    alignment=nib.Alignment.CENTER,
                ),

                # Footer row aligned to bottom
                nib.HStack(
                    controls=[
                        nib.Text("v1.0", font=nib.Font.CAPTION),
                        nib.Spacer(),
                        nib.Text("Status: OK", font=nib.Font.CAPTION),
                    ],
                    alignment=nib.VerticalAlignment.BOTTOM,
                ),
            ],
            alignment=nib.HorizontalAlignment.LEADING,
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```
