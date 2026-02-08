# Effect Modifiers

Effect modifiers add visual effects and transformations to views, including shadows, borders, blend modes, scaling, offsets, and animations.

```python
import nib

nib.VStack(
    controls=[nib.Text("Card")],
    shadow_color="black",
    shadow_radius=10,
    shadow_y=4,
    border_color="#CCCCCC",
    border_width=1,
    animation=nib.Animation.spring(),
)
```

---

## Shadow

Drop shadows are controlled by four parameters that work together. At least one shadow parameter must be set for the shadow to render.

### shadow_color

The color of the drop shadow.

| Type | Default |
|------|---------|
| `Color \| str` | `None` |

### shadow_radius

The blur radius of the shadow in points. Larger values produce softer shadows.

| Type | Default (when shadow is active) |
|------|---------|
| `float` | `4.0` |

### shadow_x

Horizontal offset of the shadow in points. Positive values shift the shadow right.

| Type | Default (when shadow is active) |
|------|---------|
| `float` | `0.0` |

### shadow_y

Vertical offset of the shadow in points. Positive values shift the shadow down.

| Type | Default (when shadow is active) |
|------|---------|
| `float` | `2.0` |

```python
# Basic shadow
nib.Rectangle(fill="white", shadow_color="black", shadow_radius=8)

# Customized shadow
nib.VStack(
    controls=[nib.Text("Elevated Card")],
    padding=16,
    background="#FFFFFF",
    corner_radius=12,
    shadow_color="black",
    shadow_radius=12,
    shadow_x=0,
    shadow_y=6,
)

# Shadow with only radius (no color)
nib.Rectangle(fill="white", shadow_radius=4)
```

---

## Border

Border modifiers draw an outline around a view's bounds. Unlike `stroke` (which is for shapes), borders work on any view type.

### border_color

The color of the border. Required for the border to render.

| Type | Default |
|------|---------|
| `Color \| str` | `None` |

### border_width

The width of the border in points.

| Type | Default (when border_color is set) |
|------|---------|
| `float` | `1.0` |

```python
# Default 1pt border
nib.Rectangle(fill="white", border_color="#CCCCCC")

# Custom border width
nib.VStack(
    controls=[nib.Text("Bordered content")],
    padding=12,
    border_color=nib.Color.RED,
    border_width=2,
    corner_radius=8,
)
```

Note: `border_width` without `border_color` has no effect.

---

## blend_mode

Controls how a view is composited with the content behind it. See [BlendMode](../types/blend-mode.md) for all available modes.

| Type | Default |
|------|---------|
| `BlendMode \| str` | `None` |

```python
nib.Rectangle(fill=nib.Color.BLUE, blend_mode=nib.BlendMode.MULTIPLY)
nib.Image(source="overlay.png", blend_mode="screen")
```

---

## scale

Applies a uniform scale transformation to a view. The view is scaled from its center point. A value of `1.0` is the original size.

| Type | Default |
|------|---------|
| `float` | `None` |

```python
nib.Image(system_name="star.fill", scale=2.0)   # Double size
nib.Text("Small", scale=0.75)                     # 75% size
```

---

## offset

Shifts a view from its natural position. The view still occupies its original space in the layout. See [Offset](../types/geometry.md) for constructor details.

| Type | Default |
|------|---------|
| `Offset` | `None` |

```python
nib.Circle(
    fill=nib.Color.BLUE,
    width=50,
    height=50,
    offset=nib.Offset(10, -5),
)
```

---

## Animation

### animation

Configures how property changes on this view are animated. Once set, the animation is "sticky" -- all future property mutations on the view animate using this configuration. See [Animation](../types/animation.md) for factory methods and presets.

| Type | Default |
|------|---------|
| `Animation` | `None` |

```python
# Spring animation on all property changes
counter = nib.Text("0", animation=nib.Animation.spring())

def increment():
    counter.content = str(int(counter.content) + 1)  # Animates automatically
```

```python
# Ease-in-out opacity toggle
box = nib.Rectangle(
    fill="blue",
    width=100,
    height=100,
    animation=nib.Animation.easeInOut(0.3),
)
```

### content_transition

Controls how a view's content animates when it changes. This is separate from view transitions -- it affects the content within a view that remains visible. See [ContentTransition](../types/transition.md#contenttransition) for all values.

| Type | Default |
|------|---------|
| `ContentTransition \| str` | `None` |

```python
# Rolling numeric digits
counter = nib.Text(
    "0",
    content_transition=nib.ContentTransition.NUMERIC_TEXT,
    animation=nib.Animation.spring(),
)

# Fading content swap
label = nib.Text("Status", content_transition=nib.ContentTransition.OPACITY)
```

### transition

Controls how a view animates when it appears in or disappears from the view hierarchy. See [Transition](../types/transition.md) for all values, asymmetric transitions, and custom keyframes.

| Type | Default |
|------|---------|
| `Transition \| str \| TransitionConfig` | `None` |

```python
# Simple fade
panel = nib.VStack(controls=[...], transition=nib.Transition.OPACITY)

# Asymmetric: slide in, fade out
panel = nib.VStack(
    controls=[...],
    transition=nib.Transition.asymmetric(
        insertion=nib.Transition.SLIDE,
        removal=nib.Transition.OPACITY,
    ),
)

# Combined: fade and scale simultaneously
badge = nib.Text(
    "New",
    transition=nib.Transition.combined(nib.Transition.OPACITY, nib.Transition.SCALE),
)
```

## Examples

### Elevated card with shadow and border

```python
import nib

def main(app: nib.App):
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Notification", font=nib.Font.HEADLINE),
                nib.Text(
                    "You have 3 new messages.",
                    foreground_color=nib.Color.SECONDARY,
                ),
            ],
            spacing=6,
            padding=16,
            background="#FFFFFF",
            corner_radius=12,
            border_color="#E0E0E0",
            border_width=1,
            shadow_color="black",
            shadow_radius=10,
            shadow_y=4,
        )
    )

nib.run(main)
```

### Animated counter with effects

```python
import nib

def main(app: nib.App):
    count = 0
    label = nib.Text(
        "0",
        font=nib.Font.system(48, nib.FontWeight.BOLD),
        content_transition=nib.ContentTransition.NUMERIC_TEXT,
        animation=nib.Animation.spring(response=0.4, damping=0.6),
    )

    def increment():
        nonlocal count
        count += 1
        label.content = str(count)

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Button(
                    "Add",
                    action=increment,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
            ],
            spacing=16,
            padding=24,
        )
    )

nib.run(main)
```

### Overlapping views with offset and blend

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(
            controls=[
                nib.Circle(fill=nib.Color.RED, width=100, height=100),
                nib.Circle(
                    fill=nib.Color.BLUE,
                    width=100,
                    height=100,
                    offset=nib.Offset(40, 0),
                    blend_mode=nib.BlendMode.SCREEN,
                ),
            ],
            padding=40,
        )
    )

nib.run(main)
```
