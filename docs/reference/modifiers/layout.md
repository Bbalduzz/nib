# Layout Modifiers

Layout modifiers control the size and spacing of views. They map to SwiftUI's `.frame()` and `.padding()` view modifiers.

```python
import nib

nib.Text("Hello", width=200, padding=16)
nib.VStack(controls=[...], min_width=300, max_width="infinity", height=400)
```

---

## Frame Modifiers

Frame modifiers set fixed or flexible dimensions on a view.

### `width`

Fixed width in points.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.Rectangle(fill="blue", width=100, height=50)
```

### `height`

Fixed height in points.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.Rectangle(fill="blue", width=100, height=50)
```

### `min_width`

Minimum width constraint in points. The view will not shrink below this size.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.TextField("Search...", text="", min_width=200)
```

### `min_height`

Minimum height constraint in points.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.TextEditor(text="", min_height=100)
```

### `max_width`

Maximum width constraint. The view will not expand beyond this size. Use `"infinity"` or `float("inf")` to fill all available horizontal space.

| Type | Default |
|------|---------|
| `float \| str` | `None` |

```python
# Fill available width
nib.Rectangle(fill="blue", max_width="infinity", height=2)

# Cap at 400 points
nib.VStack(controls=[...], max_width=400)
```

### `max_height`

Maximum height constraint. Use `"infinity"` or `float("inf")` to fill all available vertical space.

| Type | Default |
|------|---------|
| `float \| str` | `None` |

```python
nib.ScrollView(controls=[...], max_height=300)
```

### Combining frame modifiers

Frame modifiers can be combined to create flexible layouts:

```python
import nib

# Fixed size box
nib.Rectangle(fill="blue", width=100, height=100)

# Flexible width with constraints
nib.TextField("Name", text="", min_width=150, max_width=400, height=32)

# Full-width container with fixed height
nib.HStack(
    controls=[nib.Text("Left"), nib.Spacer(), nib.Text("Right")],
    max_width="infinity",
    height=44,
    padding={"horizontal": 16},
)
```

---

## Padding

Padding adds space between a view's content and its boundary. It is applied inside the view's background.

| Type | Default |
|------|---------|
| `float \| dict` | `None` |

### Uniform padding

A single numeric value applies equal padding to all four edges:

```python
nib.Text("Padded", padding=16)
```

### Edge-specific padding

A dictionary specifying individual edges. Available keys: `top`, `bottom`, `leading`, `trailing`.

```python
nib.Text("Custom padding", padding={
    "top": 8,
    "bottom": 8,
    "leading": 16,
    "trailing": 16,
})
```

### Directional padding

A dictionary with `horizontal` and/or `vertical` keys for symmetric padding:

```python
nib.Text("Directional", padding={"horizontal": 16, "vertical": 8})
```

This is equivalent to:

```python
nib.Text("Directional", padding={"leading": 16, "trailing": 16, "top": 8, "bottom": 8})
```

### Padding examples

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Uniform padding
                nib.Text("All sides: 20", background="#333", padding=20),

                # Horizontal only
                nib.Text("Horizontal: 24", background="#333", padding={"horizontal": 24}),

                # Per-edge control
                nib.Text("Custom edges", background="#333", padding={
                    "top": 4,
                    "bottom": 12,
                    "leading": 20,
                    "trailing": 8,
                }),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

---

## Margin

Margin adds space outside a view's bounds, after the background is rendered. This creates spacing between the view (including its background) and surrounding content.

| Type | Default |
|------|---------|
| `float \| dict` | `None` |

Margin supports the same formats as padding: uniform value, edge-specific dictionary, or directional dictionary.

```python
# Uniform margin
nib.Rectangle(fill="blue", width=100, height=100, margin=8)

# Directional margin
nib.Text("Spaced", background="#333", margin={"horizontal": 16, "vertical": 8})

# Edge-specific margin
nib.VStack(
    controls=[...],
    margin={"top": 0, "bottom": 20, "leading": 16, "trailing": 16},
)
```

### Padding vs. Margin

The key difference is where the space appears relative to the background:

- **Padding** is inside the background -- it increases the visible area of the background.
- **Margin** is outside the background -- it pushes the view away from its neighbors.

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                # Padding: background extends behind the padding
                nib.Text(
                    "Padding (inside bg)",
                    background="#444",
                    foreground_color="white",
                    padding=20,
                ),
                # Margin: space outside the background
                nib.Text(
                    "Margin (outside bg)",
                    background="#444",
                    foreground_color="white",
                    margin=20,
                ),
            ],
            spacing=0,
            background="#222",
            padding=16,
        )
    )

nib.run(main)
```
