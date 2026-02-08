# Modifiers

All view styling in Nib is done through constructor parameters. There is no method chaining. This is a deliberate departure from SwiftUI's `.modifier()` pattern -- Nib keeps everything in one place, making your code easier to read and modify.

```python
# SwiftUI style (NOT how Nib works):
# Text("Hello").font(.title).foregroundColor(.blue).padding(16)

# Nib style:
nib.Text(
    "Hello",
    font=nib.Font.TITLE,
    foreground_color=nib.Color.BLUE,
    padding=16,
)
```

## Layout

Control the size and spacing of views.

```python
# Fixed dimensions
nib.Text("Fixed size", width=200, height=50)

# Minimum and maximum dimensions
nib.Text("Flexible", min_width=100, max_width=300)

# Fill available width
nib.Text("Full width", max_width="infinity")

# Padding (inside background)
nib.Text("Padded", padding=16, background="#333333")

# Padding with per-side control
nib.Text("Custom padding", padding={"top": 8, "bottom": 8, "leading": 16, "trailing": 16})

# Shorthand: horizontal and vertical
nib.Text("Shorthand", padding={"horizontal": 16, "vertical": 8})

# Margin (outside background)
nib.VStack(
    controls=[nib.Text("Content")],
    background="#333333",
    padding=12,
    margin=8,  # Space outside the background
)
```

| Parameter | Type | Description |
|---|---|---|
| `width` | float | Fixed width in points |
| `height` | float | Fixed height in points |
| `min_width` | float | Minimum width |
| `min_height` | float | Minimum height |
| `max_width` | float or `"infinity"` | Maximum width |
| `max_height` | float or `"infinity"` | Maximum height |
| `padding` | float or dict | Inner spacing (inside background) |
| `margin` | float or dict | Outer spacing (outside background) |

!!! info "padding vs margin"
    `padding` is applied inside the background. If you set `background="#333"` and `padding=16`, the background extends behind the padding. `margin` is applied outside the background, creating space between the background edge and neighboring views.

## Appearance

Control colors, opacity, and corner rounding.

```python
# Background color (string, Color enum, or View)
nib.Text("Colored", background="#ff5733")
nib.Text("Themed", background=nib.Color.BLUE)

# Background as a view
nib.VStack(
    controls=[nib.Text("Fancy")],
    background=nib.Rectangle(
        corner_radius=12,
        fill="#1a1a2e",
        stroke="#2a2a4e",
        stroke_width=1,
    ),
    padding=16,
)

# Foreground color (text and content color)
nib.Text("Blue text", foreground_color=nib.Color.BLUE)
nib.Text("Hex color", foreground_color="#e74c3c")

# Shape fill and stroke
nib.Circle(fill=nib.Color.RED, stroke="#000000", stroke_width=2, width=50, height=50)

# Opacity
nib.Text("Faded", opacity=0.5)

# Corner radius
nib.VStack(
    controls=[nib.Text("Rounded")],
    corner_radius=8,
    background="#333333",
    padding=12,
)
```

| Parameter | Type | Description |
|---|---|---|
| `background` | Color, string, or View | Background fill |
| `foreground_color` | Color or string | Text/content color |
| `fill` | Color or string | Shape fill color |
| `stroke` | Color or string | Shape stroke color |
| `stroke_width` | float | Stroke width in points |
| `opacity` | float | Opacity from 0.0 to 1.0 |
| `corner_radius` | float | Corner rounding in points |

## Typography

Control font and weight.

```python
# System fonts
nib.Text("Title", font=nib.Font.TITLE)
nib.Text("Headline", font=nib.Font.HEADLINE)
nib.Text("Body", font=nib.Font.BODY)
nib.Text("Caption", font=nib.Font.CAPTION)

# Custom font with size
nib.Text("Custom", font=nib.Font.custom("Menlo", size=14))

# Font weight
nib.Text("Bold", font_weight=nib.FontWeight.BOLD)
nib.Text("Light", font_weight="light")

# Combined
nib.Text(
    "Styled",
    font=nib.Font.TITLE,
    font_weight=nib.FontWeight.HEAVY,
    foreground_color=nib.Color.BLUE,
)
```

| Parameter | Type | Description |
|---|---|---|
| `font` | Font or string | Font style or custom font |
| `font_weight` | FontWeight or string | Text weight |

## Effects

Shadows, borders, clipping, blending, and transforms.

### Shadows

```python
nib.VStack(
    controls=[nib.Text("Shadow")],
    background="#ffffff",
    padding=16,
    corner_radius=8,
    shadow_radius=10,
    shadow_color="#00000033",
    shadow_x=0,
    shadow_y=4,
)
```

### Borders

```python
nib.VStack(
    controls=[nib.Text("Bordered")],
    padding=12,
    border_color="#3498db",
    border_width=2,
)
```

### Clip Shape

```python
# Clip to circle
nib.Image("photo.jpg", width=80, height=80, clip_shape="circle")

# Clip to capsule
nib.Text("Tag", padding={"horizontal": 12, "vertical": 4}, clip_shape="capsule", background="#3498db")

# Clip to rounded rectangle
nib.Image("banner.jpg", clip_shape=nib.Rectangle(corner_radius=12))
```

### Scale and Offset

```python
# Scale
nib.SFSymbol("star.fill", scale=1.5)

# Offset (useful in ZStack for positioning)
nib.ZStack(
    controls=[
        nib.Circle(fill=nib.Color.BLUE, width=100, height=100),
        nib.Text("Centered", offset=nib.Offset(x=0, y=-10)),
    ],
)
```

### Blend Mode

```python
nib.Image("photo.jpg", blend_mode=nib.BlendMode.MULTIPLY)
```

| Parameter | Type | Description |
|---|---|---|
| `shadow_color` | string | Shadow color |
| `shadow_radius` | float | Shadow blur radius |
| `shadow_x` | float | Shadow horizontal offset |
| `shadow_y` | float | Shadow vertical offset |
| `border_color` | Color or string | Border color |
| `border_width` | float | Border width in points |
| `clip_shape` | string or View | Clip to shape (`"circle"`, `"capsule"`, or shape view) |
| `scale` | float | Scale transform factor |
| `offset` | Offset | Position offset (x, y) |
| `blend_mode` | BlendMode or string | Layer blending mode |

## Animation

Animate property changes with built-in animation support.

```python
# Animate all changes on this view
box = nib.VStack(
    controls=[nib.Text("Animated")],
    background="#333333",
    padding=16,
    opacity=1.0,
    animation=nib.Animation.EASE_IN_OUT,
)

def fade():
    box.opacity = 0.3  # Animates smoothly

# Animation with custom duration
nib.VStack(
    controls=[nib.Text("Slow")],
    animation=nib.Animation(type="easeInOut", duration=0.5),
)

# Spring animation
nib.VStack(
    controls=[nib.Text("Bouncy")],
    animation=nib.Animation(type="spring"),
)

# Content transition (how content changes animate)
counter = nib.Text("0", content_transition="numericText")

# View transition (how views appear/disappear)
nib.Text("Slides in", transition="slide")
```

!!! tip "Sticky animations"
    When you set `animation=` on a view, it becomes "sticky" -- all future property changes on that view will animate with the same configuration. You do not need to re-specify the animation on each change.

| Parameter | Type | Description |
|---|---|---|
| `animation` | Animation | Animation for property changes |
| `content_transition` | ContentTransition or string | Animation for content changes |
| `transition` | Transition or string | Animation for appear/disappear |

## Interaction

Handle user interactions directly on any view.

```python
# Drag and drop
nib.VStack(
    controls=[nib.Text("Drop files here")],
    on_drop=lambda paths: print(f"Dropped: {paths}"),
    padding=20,
    border_color="#666",
    border_width=1,
)

# Hover detection
nib.Text(
    "Hover me",
    on_hover=lambda hovering: print(f"Hovering: {hovering}"),
)

# Click handler
nib.VStack(
    controls=[nib.Text("Click me")],
    on_click=lambda: print("Clicked!"),
)

# Tooltip
nib.Button("Save", action=save, tooltip="Save the current document")
```

| Parameter | Type | Description |
|---|---|---|
| `on_drop` | callback | Receives `list[str]` of file paths |
| `on_hover` | callback | Receives `bool` (True on enter, False on exit) |
| `on_click` | callback | Called on click (no arguments) |
| `tooltip` | string or View | Tooltip shown on hover |
| `visible` | bool | Whether view is included in tree |

## Reactive Modifiers

All modifier parameters can be changed after construction, and changes trigger automatic re-renders:

```python
card = nib.VStack(
    controls=[nib.Text("Card")],
    background="#333333",
    opacity=1.0,
    padding=16,
    corner_radius=8,
)

# All of these trigger re-renders
card.opacity = 0.5
card.background = "#ff0000"
card.padding = 24
card.corner_radius = 16
card.border_color = "#ffffff"
card.border_width = 2
```

See [Reactivity](reactivity.md) for more on how property changes trigger UI updates.

## Modifier Application Order

Modifiers are applied in a specific order that matches SwiftUI conventions:

1. **Font** -- applied first so text sizing is correct
2. **Foreground color** -- text/content color
3. **Fill and stroke** -- shape colors
4. **Padding** -- inner spacing
5. **Frame** -- width, height, min/max constraints
6. **Background** -- behind padded content
7. **Corner radius** -- rounds the background
8. **Margin** -- outer spacing after background
9. **Border** -- around the outer edge
10. **Shadow** -- drop shadow behind everything
11. **Clip shape** -- clips the final result
12. **Opacity** -- applied to the entire composed view
13. **Scale, offset, blend mode** -- transforms
14. **Animation and transitions** -- animation configuration

This order means `padding` is inside `background` (padding pushes content away from background edges), and `margin` is outside `background` (margin creates space between this view and its neighbors).
