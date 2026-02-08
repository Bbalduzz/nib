# Animation

The `Animation` dataclass configures how property changes are animated. Animations control the timing curve and duration of transitions when view properties are mutated.

```python
import nib

counter = nib.Text("0", animation=nib.Animation.spring())

def increment():
    counter.content = str(int(counter.content) + 1)  # Change animates automatically
```

## Constructor

```python
Animation(type, duration=None, delay=None, response=None, damping=None)
```

The `Animation` dataclass is not typically constructed directly. Use the factory methods below instead.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `type` | `str` | -- | Animation type: `"linear"`, `"easeIn"`, `"easeOut"`, `"easeInOut"`, or `"spring"`. |
| `duration` | `float` | `None` | Duration in seconds (for timing-curve animations). |
| `delay` | `float` | `None` | Delay before the animation starts, in seconds. |
| `response` | `float` | `None` | Spring response time -- how quickly the spring settles (spring animations only). |
| `damping` | `float` | `None` | Spring damping fraction -- how much the spring bounces (spring animations only). |

## Factory Methods

### `Animation.linear(duration=0.3)`

Create a linear animation with constant speed.

```python
anim = nib.Animation.linear(0.5)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | `float` | `0.3` | Duration in seconds. |

### `Animation.easeIn(duration=0.3)`

Create an ease-in animation that starts slow and accelerates.

```python
anim = nib.Animation.easeIn(0.3)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | `float` | `0.3` | Duration in seconds. |

### `Animation.easeOut(duration=0.3)`

Create an ease-out animation that starts fast and decelerates.

```python
anim = nib.Animation.easeOut(0.2)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | `float` | `0.3` | Duration in seconds. |

### `Animation.easeInOut(duration=0.3)`

Create an ease-in-out animation that starts and ends slowly with faster motion in the middle.

```python
anim = nib.Animation.easeInOut(0.4)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | `float` | `0.3` | Duration in seconds. |

### `Animation.spring(response=0.3, damping=0.7)`

Create a spring animation with physics-based timing. Spring animations feel more natural than timing curves.

```python
anim = nib.Animation.spring()                    # Default spring
anim = nib.Animation.spring(response=0.5, damping=0.6)  # Custom spring
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `response` | `float` | `0.3` | How quickly the spring settles (lower values = faster). |
| `damping` | `float` | `0.7` | How much the spring bounces. `0.0` = oscillates forever, `1.0` = no bounce (critical damping). |

## Presets

Nib provides four built-in animation presets as class attributes:

| Preset | Equivalent | Description |
|--------|-----------|-------------|
| `Animation.default` | `Animation.easeInOut(0.3)` | Standard animation for most UI changes. |
| `Animation.fast` | `Animation.easeOut(0.15)` | Quick animation for responsive feedback. |
| `Animation.slow` | `Animation.easeInOut(0.5)` | Slower animation for emphasis. |
| `Animation.bouncy` | `Animation.spring(0.3, 0.5)` | Bouncy spring animation. |

```python
nib.Text("Quick", animation=nib.Animation.fast)
nib.Text("Bouncy", animation=nib.Animation.bouncy)
```

## Sticky Animations

When an animation is set on a view, it becomes "sticky" -- all future property changes on that view are animated using the same configuration. This means you only need to set the animation once.

```python
import nib

def main(app: nib.App):
    # Animation is set once and applies to all future mutations
    label = nib.Text("0", font=nib.Font.TITLE, animation=nib.Animation.spring())

    def increment():
        label.content = str(int(label.content) + 1)  # Animates with spring

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Button("Increment", action=increment),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

## Examples

### Animated counter with numeric text transition

```python
import nib

def main(app: nib.App):
    count = nib.Text(
        "0",
        font=nib.Font.system(48, nib.FontWeight.BOLD),
        animation=nib.Animation.spring(response=0.4, damping=0.6),
        content_transition=nib.ContentTransition.NUMERIC_TEXT,
    )

    def increment():
        count.content = str(int(count.content) + 1)

    app.build(
        nib.VStack(
            controls=[count, nib.Button("Add", action=increment)],
            spacing=16,
            padding=20,
        )
    )

nib.run(main)
```

### Animated opacity toggle

```python
import nib

def main(app: nib.App):
    box = nib.Rectangle(
        fill=nib.Color.BLUE,
        width=100,
        height=100,
        corner_radius=12,
        animation=nib.Animation.easeInOut(0.4),
    )

    def toggle():
        box.opacity = 0.2 if (box.opacity or 1.0) > 0.5 else 1.0

    app.build(
        nib.VStack(
            controls=[box, nib.Button("Toggle", action=toggle)],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```
