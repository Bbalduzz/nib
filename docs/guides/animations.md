# Animations & Transitions

Nib supports three categories of animation: property animations that interpolate value changes, content transitions that animate text and content swaps, and view transitions that animate when views appear or disappear.

---

## Animation Class

The `Animation` class defines timing curves. Apply it to any view with the `animation` parameter. When a property of that view changes, the change is animated.

```python
import nib

counter = nib.Text("0", animation=nib.Animation.spring())
```

### Timing curves

| Factory method | Behavior |
|---------------|----------|
| `Animation.linear(duration)` | Constant speed |
| `Animation.easeIn(duration)` | Slow start, fast end |
| `Animation.easeOut(duration)` | Fast start, slow end |
| `Animation.easeInOut(duration)` | Slow start and end |
| `Animation.spring(response, damping)` | Physics-based spring |

All timing curves accept a `duration` parameter in seconds (default: `0.3`):

```python
nib.Animation.linear(duration=0.5)
nib.Animation.easeInOut(duration=1.0)
nib.Animation.easeOut(duration=0.15)
```

### Spring animation

Spring animations have two parameters:

- `response` -- how quickly the spring settles (lower = faster, default `0.3`)
- `damping` -- how much the spring bounces (`0.0` = bounces forever, `1.0` = no bounce, default `0.7`)

```python
# Snappy spring with slight bounce
nib.Animation.spring(response=0.3, damping=0.7)

# Bouncy spring
nib.Animation.spring(response=0.4, damping=0.4)

# Stiff spring, no bounce
nib.Animation.spring(response=0.2, damping=1.0)
```

### Presets

Four presets are available for common cases:

```python
nib.Animation.default   # easeInOut(0.3)
nib.Animation.fast      # easeOut(0.15)
nib.Animation.slow      # easeInOut(0.5)
nib.Animation.bouncy    # spring(response=0.3, damping=0.5)
```

### Example: Animated counter

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("number")
    app.width = 200
    app.height = 150

    count = 0
    label = nib.Text("0", font=nib.Font.LARGE_TITLE, animation=nib.Animation.spring())

    def increment():
        nonlocal count
        count += 1
        label.content = str(count)

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Button("Add", action=increment),
            ],
            spacing=16,
            padding=24,
        )
    )

nib.run(main)
```

---

## Content Transitions

Content transitions animate how the content of a view changes. They are most useful with `Text` views when the displayed value updates.

Apply with the `content_transition` parameter:

```python
nib.Text("42", content_transition=nib.ContentTransition.NUMERIC_TEXT)
```

| Transition | Effect |
|-----------|--------|
| `ContentTransition.IDENTITY` | No animation (default) |
| `ContentTransition.INTERPOLATE` | Smoothly interpolate between old and new content |
| `ContentTransition.OPACITY` | Cross-fade between old and new content |
| `ContentTransition.NUMERIC_TEXT` | Roll digits up when numbers increase |
| `ContentTransition.NUMERIC_TEXT_DOWN` | Roll digits down when numbers decrease |

### Numeric text transition

`NUMERIC_TEXT` is ideal for counters, timers, and scores. Digits roll upward when the number increases:

```python
import nib

def main(app: nib.App):
    app.title = "Score"
    app.icon = nib.SFSymbol("star")
    app.width = 200
    app.height = 150

    score = 0
    score_label = nib.Text(
        "0",
        font=nib.Font.system(48, nib.FontWeight.BOLD),
        content_transition=nib.ContentTransition.NUMERIC_TEXT,
        animation=nib.Animation.spring(),
    )

    def add_point():
        nonlocal score
        score += 10
        score_label.content = str(score)

    app.build(
        nib.VStack(
            controls=[score_label, nib.Button("+10", action=add_point)],
            spacing=16,
            padding=24,
        )
    )

nib.run(main)
```

!!! tip
    Pair `content_transition` with `animation` for the best effect. The animation controls the timing curve, while the content transition controls the visual style.

---

## View Transitions

View transitions animate when a view appears or disappears from the view hierarchy. Apply with the `transition` parameter.

```python
nib.Text("Appearing!", transition=nib.Transition.OPACITY)
```

### Simple transitions

| Transition | Effect |
|-----------|--------|
| `Transition.IDENTITY` | No animation |
| `Transition.OPACITY` | Fade in/out |
| `Transition.SCALE` | Scale up from center on appear, scale down on disappear |
| `Transition.SLIDE` | Slide in from leading edge, slide out to trailing edge |
| `Transition.MOVE_LEADING` | Move in from the left |
| `Transition.MOVE_TRAILING` | Move in from the right |
| `Transition.MOVE_TOP` | Move in from the top |
| `Transition.MOVE_BOTTOM` | Move in from the bottom |
| `Transition.PUSH` | Push new content in, push old content out |

### Asymmetric transitions

Use different animations for appearing and disappearing:

```python
nib.Text(
    "Slide in, fade out",
    transition=nib.Transition.asymmetric(
        insertion=nib.Transition.SLIDE,
        removal=nib.Transition.OPACITY,
    ),
)

nib.Text(
    "Scale in, move out",
    transition=nib.Transition.asymmetric(
        insertion=nib.Transition.SCALE,
        removal=nib.Transition.MOVE_BOTTOM,
    ),
)
```

### Combined transitions

Apply multiple transition effects simultaneously:

```python
nib.Text(
    "Fade and scale together",
    transition=nib.Transition.combined(
        nib.Transition.OPACITY,
        nib.Transition.SCALE,
    ),
)
```

### Custom keyframe transitions

Build fully custom transitions with keyframe interpolation:

```python
# Custom swoosh transition
swoosh = (
    nib.Transition.custom("swoosh")
    .at(0.0, opacity=0, scale=0.5, offset_x=-50)
    .at(0.5, opacity=1, scale=1.1, offset_x=10)
    .at(1.0, opacity=1, scale=1.0, offset_x=0)
    .build()
)

nib.Text("Swoosh!", transition=swoosh)
```

Keyframe properties:

| Property | Description |
|----------|-------------|
| `opacity` | View opacity (0.0 to 1.0) |
| `scale` | Scale factor (1.0 = normal) |
| `blur` | Gaussian blur radius |
| `offset_x` | Horizontal offset in points |
| `offset_y` | Vertical offset in points |

### Pre-built custom transitions

Nib includes two ready-made custom transitions:

```python
# Pop-fade: scales up slightly while fading in
nib.Text("Pop!", transition=nib.Transition.pop_fade())

# Bounce-in: overshoots then settles
nib.Text("Bounce!", transition=nib.Transition.bounce_in())
```

---

## Example: Animated Visibility Toggle

Combine `animation` and `transition` with the `visible` property to animate showing and hiding views:

```python
import nib

def main(app: nib.App):
    app.title = "Toggle View"
    app.icon = nib.SFSymbol("eye")
    app.width = 280
    app.height = 250

    detail = nib.VStack(
        controls=[
            nib.Text("Detail Panel", font=nib.Font.HEADLINE),
            nib.Text("This panel fades and scales in.",
                      foreground_color=nib.Color.SECONDARY),
        ],
        spacing=8,
        padding=16,
        background=nib.Rectangle(corner_radius=10, fill="#1c1c1e"),
        transition=nib.Transition.combined(nib.Transition.OPACITY, nib.Transition.SCALE),
        animation=nib.Animation.spring(),
    )

    def toggle():
        detail.visible = not detail.visible

    app.build(
        nib.VStack(
            controls=[
                nib.Button("Toggle Detail", action=toggle),
                detail,
            ],
            spacing=16,
            padding=24,
            animation=nib.Animation.easeInOut(0.3),
        )
    )

nib.run(main)
```
