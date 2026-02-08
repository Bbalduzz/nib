# Transition

The `Transition` enum and `TransitionConfig` dataclass control how views animate when they appear in or disappear from the view hierarchy. The related `ContentTransition` enum controls how a view's content animates when it changes.

```python
import nib

# Simple transition
label = nib.Text("Hello", transition=nib.Transition.OPACITY)

# Asymmetric transition
panel = nib.VStack(
    controls=[...],
    transition=nib.Transition.asymmetric(
        insertion=nib.Transition.SLIDE,
        removal=nib.Transition.OPACITY,
    ),
)
```

## Transition Enum

The `Transition` enum defines built-in transition animations.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `Transition.IDENTITY` | `.identity` | No animation (instant appear/disappear). |
| `Transition.OPACITY` | `.opacity` | Fade in/out. |
| `Transition.SCALE` | `.scale` | Scale up from zero / shrink to zero. |
| `Transition.SLIDE` | `.slide` | Slide in from the leading edge / out to the trailing edge. |
| `Transition.MOVE_LEADING` | `.move(edge: .leading)` | Move in from the leading edge. |
| `Transition.MOVE_TRAILING` | `.move(edge: .trailing)` | Move in from the trailing edge. |
| `Transition.MOVE_TOP` | `.move(edge: .top)` | Move in from the top edge. |
| `Transition.MOVE_BOTTOM` | `.move(edge: .bottom)` | Move in from the bottom edge. |
| `Transition.PUSH` | `.push` | Push transition (content slides in, replacing previous). |

```python
nib.Text("Fade", transition=nib.Transition.OPACITY)
nib.Text("Scale", transition=nib.Transition.SCALE)
nib.Text("Slide In", transition=nib.Transition.MOVE_LEADING)
```

## Static Methods

### `Transition.asymmetric(insertion, removal)`

Create a transition with different animations for insertion (appearing) and removal (disappearing).

```python
transition = nib.Transition.asymmetric(
    insertion=nib.Transition.SCALE,
    removal=nib.Transition.OPACITY,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `insertion` | `Transition \| str` | Transition used when the view appears. |
| `removal` | `Transition \| str` | Transition used when the view disappears. |

**Returns:** A `TransitionConfig` object.

### `Transition.combined(*transitions)`

Create a transition that combines multiple transition effects simultaneously.

```python
transition = nib.Transition.combined(nib.Transition.OPACITY, nib.Transition.SCALE)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `*transitions` | `Transition \| str` | Two or more transition types to combine. |

**Returns:** A `TransitionConfig` object.

### `Transition.custom(name)`

Start building a custom keyframe-based transition. Returns a `CustomTransitionBuilder` for method chaining.

```python
transition = (
    nib.Transition.custom("swoosh")
    .at(0.0, opacity=0, scale=0.5, offset_x=-50)
    .at(0.5, opacity=1, scale=1.1, offset_x=10)
    .at(1.0, opacity=1, scale=1.0, offset_x=0)
    .build()
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Name for the custom transition (used for debugging). |

**Returns:** A `CustomTransitionBuilder`.

### `Transition.pop_fade()`

Pre-built transition that scales up slightly while fading in.

```python
panel = nib.VStack(controls=[...], transition=nib.Transition.pop_fade())
```

### `Transition.bounce_in()`

Pre-built transition that overshoots then settles into place.

```python
badge = nib.Text("New", transition=nib.Transition.bounce_in())
```

## TransitionConfig

The `TransitionConfig` dataclass represents advanced transition configurations that cannot be expressed as a single enum value.

| Field | Type | Description |
|-------|------|-------------|
| `config_type` | `str` | `"simple"`, `"asymmetric"`, `"combined"`, or `"custom"`. |
| `value` | `str` | Transition value for `"simple"` type. |
| `insertion` | `str` | Insertion transition for `"asymmetric"` type. |
| `removal` | `str` | Removal transition for `"asymmetric"` type. |
| `transitions` | `list[str]` | List of transitions for `"combined"` type. |
| `keyframes` | `list[dict]` | Keyframe data for `"custom"` type. |

### Class Methods

```python
TransitionConfig.simple("opacity")
TransitionConfig.asymmetric("scale", "opacity")
TransitionConfig.combined("opacity", "scale")
```

You typically do not construct `TransitionConfig` directly. Use `Transition.asymmetric()`, `Transition.combined()`, or `Transition.custom()` instead.

## CustomTransitionBuilder

The builder class for creating keyframe-based custom transitions.

### `.at(progress, *, opacity=None, scale=None, blur=None, offset_x=None, offset_y=None)`

Add a keyframe at the given progress point.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `progress` | `float` | -- | Progress value from `0.0` (start) to `1.0` (end). |
| `opacity` | `float` | `None` | Opacity at this keyframe (0.0--1.0). |
| `scale` | `float` | `None` | Scale at this keyframe (1.0 = normal). |
| `blur` | `float` | `None` | Blur radius at this keyframe. |
| `offset_x` | `float` | `None` | Horizontal offset at this keyframe. |
| `offset_y` | `float` | `None` | Vertical offset at this keyframe. |

**Returns:** `self` (for method chaining).

### `.build()`

Build and return the final `TransitionConfig`. Raises `ValueError` if no keyframes have been defined.

## ContentTransition

The `ContentTransition` enum controls how a view's content animates when it changes. This is separate from the view transition -- it affects the content within a view that remains visible.

| Value | SwiftUI Equivalent | Description |
|-------|-------------------|-------------|
| `ContentTransition.IDENTITY` | `.identity` | No content animation. |
| `ContentTransition.INTERPOLATE` | `.interpolate` | Smooth interpolation between old and new content. |
| `ContentTransition.NUMERIC_TEXT` | `.numericText()` | Digits roll upward when increasing. |
| `ContentTransition.NUMERIC_TEXT_DOWN` | `.numericText(countsDown: true)` | Digits roll downward when decreasing. |
| `ContentTransition.OPACITY` | `.opacity` | Old content fades out, new content fades in. |

```python
# Counter with rolling digits
counter = nib.Text("0", content_transition=nib.ContentTransition.NUMERIC_TEXT)

# Fading content changes
status = nib.Text("Ready", content_transition=nib.ContentTransition.OPACITY)
```

## Examples

### Asymmetric slide transition

```python
import nib

def main(app: nib.App):
    panel = nib.VStack(
        controls=[nib.Text("Panel Content", padding=20)],
        background="#262626",
        corner_radius=12,
        transition=nib.Transition.asymmetric(
            insertion=nib.Transition.MOVE_TRAILING,
            removal=nib.Transition.MOVE_LEADING,
        ),
        animation=nib.Animation.spring(),
    )

    app.build(panel)

nib.run(main)
```

### Combined fade-and-scale

```python
import nib

def main(app: nib.App):
    badge = nib.Text(
        "New",
        font=nib.Font.CAPTION,
        foreground_color=nib.Color.WHITE,
        background=nib.Color.RED,
        padding={"horizontal": 8, "vertical": 4},
        corner_radius=8,
        transition=nib.Transition.combined(
            nib.Transition.OPACITY,
            nib.Transition.SCALE,
        ),
        animation=nib.Animation.spring(response=0.4, damping=0.6),
    )

    app.build(badge)

nib.run(main)
```

### Custom keyframe transition

```python
import nib

slide_fade = (
    nib.Transition.custom("slideFade")
    .at(0.0, opacity=0, offset_x=-100)
    .at(0.3, opacity=0.5, offset_x=-20)
    .at(1.0, opacity=1, offset_x=0)
    .build()
)

def main(app: nib.App):
    app.build(
        nib.Text("Animated Entry", transition=slide_fade, animation=nib.Animation.easeOut(0.5))
    )

nib.run(main)
```
