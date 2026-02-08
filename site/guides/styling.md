# Styling & Theming

All styling in Nib is done through constructor parameters. There is no method chaining -- you pass modifiers directly when creating a view.

```python
nib.Text(
    "Hello",
    font=nib.Font.TITLE,
    foreground_color=nib.Color.BLUE,
    padding=16,
    background=nib.Color.BLACK,
)
```

This guide covers the full set of appearance modifiers available on every view.

---

## Background

The `background` parameter accepts a color string, a `Color` object, or a shape view (like `Rectangle`) for richer backgrounds.

```python
# Solid named color
nib.Text("Hello", background=nib.Color.BLUE)

# Hex string
nib.Text("Hello", background="#FF5733")

# Shape with fill
nib.VStack(
    controls=[nib.Text("Card content")],
    background=nib.Rectangle(corner_radius=10, fill="blue"),
    padding=16,
)

# Shape with fill and stroke
nib.VStack(
    controls=[nib.Text("Bordered card")],
    background=nib.Rectangle(
        corner_radius=8,
        fill="#1a1a1a",
        stroke="#383838",
        stroke_width=1,
    ),
    padding=16,
)
```

!!! tip
    Use a `Rectangle` background with `corner_radius` when you want rounded corners, fill color, and stroke all in one. The `padding` modifier adds space between the content and the background edge.

---

## Foreground Color

`foreground_color` sets the color of text, icons, and other rendered content.

```python
nib.Text("Warning", foreground_color=nib.Color.RED)
nib.Text("Muted", foreground_color=nib.Color.SECONDARY)
nib.SFSymbol("star.fill", foreground_color="#FFD700")
```

---

## Opacity

`opacity` controls view transparency. Values range from `0.0` (fully transparent) to `1.0` (fully opaque).

```python
nib.Text("Ghost text", opacity=0.5)

nib.Rectangle(
    corner_radius=8,
    fill=nib.Color.BLACK,
    opacity=0.3,
    width=200,
    height=100,
)
```

You can also use `Color.with_opacity()` for per-color transparency:

```python
nib.Text("Tinted", foreground_color=nib.Color.BLUE.with_opacity(0.6))
```

---

## Corner Radius

`corner_radius` rounds the corners of any view. Pass a single float for uniform corners or a `CornerRadius` object for per-corner control.

```python
# Uniform corners
nib.Rectangle(fill=nib.Color.BLUE, corner_radius=10, width=100, height=60)

# Per-corner control
nib.Rectangle(
    fill=nib.Color.GREEN,
    corner_radius=nib.CornerRadius(
        top_left=20,
        top_right=20,
        bottom_left=0,
        bottom_right=0,
    ),
    width=100,
    height=60,
)
```

`CornerRadius` factory methods for common patterns:

```python
# All corners equal
nib.CornerRadius.all(12)

# Only specific corners
nib.CornerRadius.only(top_left=16, top_right=16)

# Top rounded, bottom square
nib.CornerRadius.vertical(top=16, bottom=0)

# Left rounded, right square
nib.CornerRadius.horizontal(left=12, right=0)
```

---

## Border

`border_color` and `border_width` add a stroke around the view's bounds.

```python
nib.Text(
    "Bordered",
    border_color="#333333",
    border_width=1,
    padding=12,
)

nib.VStack(
    controls=[nib.Text("Content")],
    border_color=nib.Color.BLUE,
    border_width=2,
    corner_radius=8,
    padding=16,
)
```

!!! note
    For rounded borders, combine `border_color` and `border_width` with `corner_radius`, or use a `Rectangle` background with `corner_radius`, `stroke`, and `stroke_width`.

---

## Shadow

Drop shadows are controlled by four parameters: `shadow_color`, `shadow_radius`, `shadow_x`, and `shadow_y`.

```python
nib.VStack(
    controls=[nib.Text("Elevated card")],
    padding=16,
    background=nib.Rectangle(corner_radius=10, fill="#ffffff"),
    shadow_color="black",
    shadow_radius=5,
    shadow_x=0,
    shadow_y=2,
)
```

A subtle shadow:

```python
nib.Rectangle(
    corner_radius=12,
    fill="#1e1e1e",
    width=200,
    height=120,
    shadow_color="#000000",
    shadow_radius=10,
    shadow_x=0,
    shadow_y=4,
)
```

---

## Clip Shape

`clip_shape` clips a view to a specific shape, hiding anything outside the boundary.

```python
# Clip to circle
nib.Image(url="https://example.com/avatar.jpg", width=64, height=64, clip_shape="circle")

# Clip to capsule (pill shape)
nib.Text("Tag", padding=8, background=nib.Color.BLUE, clip_shape="capsule")
```

Supported string values: `"circle"`, `"capsule"`.

You can also pass a shape view for more control:

```python
nib.Image(
    url="https://example.com/photo.jpg",
    width=100,
    height=100,
    clip_shape=nib.Rectangle(corner_radius=16),
)
```

---

## Scale

`scale` applies a uniform scale transform. A value of `1.0` is normal size.

```python
nib.SFSymbol("star.fill", scale=2.0)  # Double size
nib.Text("Small", scale=0.75)          # 75% size
```

---

## Blend Mode

`blend_mode` controls how a view composites with views behind it.

```python
nib.Rectangle(
    fill=nib.Color.RED,
    width=100,
    height=100,
    blend_mode=nib.BlendMode.MULTIPLY,
)
```

Available blend modes: `NORMAL`, `MULTIPLY`, `SCREEN`, `OVERLAY`, `DARKEN`, `LIGHTEN`, `COLOR_DODGE`, `COLOR_BURN`, `SOFT_LIGHT`, `HARD_LIGHT`, `DIFFERENCE`, `EXCLUSION`, `HUE`, `SATURATION`, `COLOR`, `LUMINOSITY`.

---

## Padding and Margin

`padding` adds space inside the view (between content and background). `margin` adds space outside (after the background).

```python
# Uniform padding on all sides
nib.Text("Padded", padding=16, background=nib.Color.BLUE)

# Per-side padding using a dict
nib.Text(
    "Custom padding",
    padding={"top": 8, "bottom": 8, "leading": 16, "trailing": 16},
    background=nib.Color.BLUE,
)

# Shorthand: horizontal and vertical
nib.Text(
    "Shorthand",
    padding={"horizontal": 16, "vertical": 8},
    background=nib.Color.BLUE,
)
```

---

## Width and Height

Fixed dimensions, minimums, and maximums:

```python
# Fixed size
nib.Rectangle(fill=nib.Color.RED, width=100, height=50)

# Minimum and maximum
nib.Text("Flexible", min_width=100, max_width=300)

# Fill available width
nib.Text("Full width", max_width="infinity")
```

---

## Full Styled Card Example

Combining multiple modifiers to build a polished card component:

```python
import nib

def main(app: nib.App):
    app.title = "Styled Card"
    app.icon = nib.SFSymbol("rectangle.fill")
    app.width = 320
    app.height = 300

    app.build(
        nib.VStack(
            controls=[
                nib.VStack(
                    controls=[
                        nib.HStack(
                            controls=[
                                nib.SFSymbol(
                                    "bolt.fill",
                                    foreground_color=nib.Color.YELLOW,
                                    font=nib.Font.TITLE,
                                ),
                                nib.VStack(
                                    controls=[
                                        nib.Text("Performance", font=nib.Font.HEADLINE),
                                        nib.Text("System stats", font=nib.Font.CAPTION,
                                                  foreground_color=nib.Color.SECONDARY),
                                    ],
                                    alignment=nib.HorizontalAlignment.LEADING,
                                    spacing=2,
                                ),
                                nib.Spacer(),
                                nib.Text("98%", font=nib.Font.TITLE,
                                          foreground_color=nib.Color.GREEN),
                            ],
                            spacing=12,
                            alignment=nib.VerticalAlignment.CENTER,
                        ),
                        nib.Divider(),
                        nib.HStack(
                            controls=[
                                _metric("CPU", "12%"),
                                _metric("RAM", "4.2 GB"),
                                _metric("Disk", "128 GB"),
                            ],
                            spacing=16,
                        ),
                    ],
                    spacing=12,
                    padding=16,
                    background=nib.Rectangle(
                        corner_radius=12,
                        fill="#1c1c1e",
                        stroke="#2c2c2e",
                        stroke_width=1,
                    ),
                    shadow_color="#000000",
                    shadow_radius=8,
                    shadow_y=4,
                ),
            ],
            padding=16,
        )
    )

def _metric(label, value):
    return nib.VStack(
        controls=[
            nib.Text(value, font=nib.Font.system(14, nib.FontWeight.SEMIBOLD)),
            nib.Text(label, font=nib.Font.CAPTION,
                      foreground_color=nib.Color.SECONDARY),
        ],
        spacing=2,
    )

nib.run(main)
```
