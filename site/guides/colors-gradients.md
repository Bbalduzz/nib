# Colors & Gradients

Nib supports named colors, hex strings, RGB/RGBA constructors, semantic system colors, and three gradient types. Colors can be used anywhere a color parameter is accepted: `foreground_color`, `background`, `fill`, `stroke`, `border_color`, `shadow_color`, and more.

---

## Named Colors

Use constants on the `Color` class for standard SwiftUI colors:

```python
import nib

nib.Text("Red", foreground_color=nib.Color.RED)
nib.Text("Blue", foreground_color=nib.Color.BLUE)
nib.Rectangle(fill=nib.Color.GREEN, width=50, height=50)
```

Full list of named colors:

| Color | Constant |
|-------|----------|
| Red | `nib.Color.RED` |
| Blue | `nib.Color.BLUE` |
| Green | `nib.Color.GREEN` |
| Yellow | `nib.Color.YELLOW` |
| Orange | `nib.Color.ORANGE` |
| Purple | `nib.Color.PURPLE` |
| Pink | `nib.Color.PINK` |
| White | `nib.Color.WHITE` |
| Black | `nib.Color.BLACK` |
| Gray | `nib.Color.GRAY` |
| Clear (transparent) | `nib.Color.CLEAR` |
| Indigo | `nib.Color.INDIGO` |
| Cyan | `nib.Color.CYAN` |
| Mint | `nib.Color.MINT` |
| Teal | `nib.Color.TEAL` |
| Brown | `nib.Color.BROWN` |

---

## Semantic Colors

Semantic colors adapt automatically to light and dark mode:

```python
nib.Text("Primary text", foreground_color=nib.Color.PRIMARY)
nib.Text("Secondary text", foreground_color=nib.Color.SECONDARY)
nib.Button("Action", foreground_color=nib.Color.ACCENT)
```

| Semantic | Constant | Adapts to |
|----------|----------|-----------|
| Primary | `nib.Color.PRIMARY` | Main text color |
| Secondary | `nib.Color.SECONDARY` | Dimmed/muted text |
| Accent | `nib.Color.ACCENT` | System accent color |

---

## Hex Colors

Create colors from hex strings with or without the `#` prefix:

```python
# Using the constructor
nib.Text("Custom Blue", foreground_color=nib.Color(hex="#4287f5"))
nib.Text("No hash", foreground_color=nib.Color(hex="4287f5"))

# With alpha channel (ARGB format)
nib.Rectangle(fill=nib.Color(hex="#7fff6666"), width=100, height=50)
```

---

## RGB and RGBA

Create colors from integer RGB values (0--255) or with a float alpha (0.0--1.0):

```python
# RGB (opaque)
custom_blue = nib.Color.rgb(66, 135, 245)
nib.Text("RGB Blue", foreground_color=custom_blue)

# RGBA (with transparency)
semi_red = nib.Color.rgba(255, 0, 0, 0.5)
nib.Rectangle(fill=semi_red, width=100, height=50)
```

---

## String Shortcuts

Many color parameters also accept plain strings for convenience. Named color strings and hex strings both work:

```python
# Named color string
nib.Text("Red text", foreground_color="red")

# Hex string
nib.VStack(
    controls=[nib.Text("Custom")],
    background="#FF5733",
)
```

!!! info
    String shortcuts are resolved by the Swift runtime. They support all SwiftUI color names and hex values.

---

## Color with Opacity

Use `with_opacity()` to create a translucent variant of any color:

```python
# 50% transparent indigo
nib.Rectangle(fill=nib.Color.INDIGO.with_opacity(0.5), width=100, height=50)

# Works with hex colors too
nib.Rectangle(fill=nib.Color(hex="#4287f5").with_opacity(0.8), width=100, height=50)
```

---

## LinearGradient

`LinearGradient` transitions colors along a straight line. The `start` and `end` points use unit coordinates where `(0, 0)` is top-left and `(1, 1)` is bottom-right.

```python
# Top-to-bottom gradient (default direction)
nib.LinearGradient(
    colors=[nib.Color.RED, nib.Color.BLUE],
    width=200,
    height=100,
)

# Left-to-right gradient
nib.LinearGradient(
    colors=["#FF0000", "#0000FF"],
    start=(0, 0.5),
    end=(1, 0.5),
    width=200,
    height=100,
)

# Diagonal gradient
nib.LinearGradient(
    colors=[nib.Color.ORANGE, nib.Color.PURPLE],
    start=(0, 0),
    end=(1, 1),
    width=200,
    height=100,
)
```

### Gradient Stops

For precise control over color positions, use `stops` instead of `colors`. Each stop is a tuple of `(position, color)` where position ranges from 0.0 to 1.0:

```python
nib.LinearGradient(
    stops=[
        (0.0, "#FF0000"),
        (0.3, "#FFFF00"),
        (0.7, "#00FF00"),
        (1.0, "#0000FF"),
    ],
    width=200,
    height=100,
)
```

---

## RadialGradient

`RadialGradient` radiates colors outward from a center point:

```python
nib.RadialGradient(
    colors=[nib.Color.WHITE, nib.Color.BLACK],
    center=(0.5, 0.5),
    start_radius=0,
    end_radius=100,
    width=200,
    height=200,
)
```

Off-center spotlight effect:

```python
nib.RadialGradient(
    colors=["#FFD700", "#000000"],
    center=(0.3, 0.3),
    start_radius=0,
    end_radius=150,
    width=200,
    height=200,
)
```

---

## AngularGradient

`AngularGradient` (conic gradient) rotates colors around a center point:

```python
# Full color wheel
nib.AngularGradient(
    colors=["red", "yellow", "green", "cyan", "blue", "magenta", "red"],
    center=(0.5, 0.5),
    width=200,
    height=200,
)

# Partial arc
nib.AngularGradient(
    colors=[nib.Color.BLUE, nib.Color.PURPLE],
    center=(0.5, 0.5),
    start_angle=0,
    end_angle=180,
    width=200,
    height=200,
)
```

---

## Gradients as Backgrounds

Gradient views can be used as `background` on any container:

```python
nib.VStack(
    controls=[
        nib.Text("Gradient Card", font=nib.Font.TITLE, foreground_color=nib.Color.WHITE),
        nib.Text("With smooth colors", foreground_color=nib.Color.WHITE.with_opacity(0.8)),
    ],
    spacing=8,
    padding=24,
    background=nib.LinearGradient(
        colors=["#667eea", "#764ba2"],
        start=(0, 0),
        end=(1, 1),
    ),
    corner_radius=16,
)
```

---

## Gradients as Shape Fills

Use gradients inside shapes for filled gradient shapes:

```python
nib.Rectangle(
    corner_radius=12,
    width=200,
    height=100,
    background=nib.LinearGradient(
        colors=[nib.Color.CYAN, nib.Color.BLUE],
    ),
)
```

---

## Full Example

A complete app showing various color and gradient techniques:

```python
import nib

def main(app: nib.App):
    app.title = "Colors"
    app.icon = nib.SFSymbol("paintpalette")
    app.width = 300
    app.height = 400

    app.build(
        nib.ScrollView(
            controls=[
                nib.VStack(
                    controls=[
                        # Named colors row
                        nib.HStack(
                            controls=[
                                _swatch(nib.Color.RED),
                                _swatch(nib.Color.ORANGE),
                                _swatch(nib.Color.YELLOW),
                                _swatch(nib.Color.GREEN),
                                _swatch(nib.Color.BLUE),
                                _swatch(nib.Color.PURPLE),
                            ],
                            spacing=4,
                        ),

                        # Linear gradient
                        nib.LinearGradient(
                            colors=["#FF6B6B", "#4ECDC4"],
                            start=(0, 0.5),
                            end=(1, 0.5),
                            height=60,
                            corner_radius=8,
                        ),

                        # Radial gradient
                        nib.RadialGradient(
                            colors=[nib.Color.WHITE, nib.Color.INDIGO],
                            center=(0.5, 0.5),
                            start_radius=0,
                            end_radius=120,
                            height=120,
                            corner_radius=8,
                        ),

                        # Angular gradient
                        nib.AngularGradient(
                            colors=["red", "yellow", "green", "cyan", "blue", "magenta", "red"],
                            center=(0.5, 0.5),
                            height=120,
                            corner_radius=8,
                        ),

                        # Gradient card
                        nib.VStack(
                            controls=[
                                nib.Text("Gradient Card", font=nib.Font.HEADLINE,
                                          foreground_color=nib.Color.WHITE),
                                nib.Text("Beautiful colors", font=nib.Font.CAPTION,
                                          foreground_color=nib.Color.WHITE.with_opacity(0.7)),
                            ],
                            spacing=4,
                            padding=20,
                            background=nib.LinearGradient(
                                colors=["#6366f1", "#a855f7", "#ec4899"],
                                start=(0, 0),
                                end=(1, 1),
                            ),
                            corner_radius=12,
                        ),
                    ],
                    spacing=12,
                    padding=16,
                ),
            ],
        )
    )

def _swatch(color):
    return nib.Circle(fill=color, width=36, height=36)

nib.run(main)
```
