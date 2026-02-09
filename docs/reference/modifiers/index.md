# Modifiers Reference

Modifiers are constructor parameters shared by all Nib views. They control layout, appearance, typography, effects, and animation. Every view inherits these parameters from the base `View` class.

```python
import nib

nib.Text(
    "Hello",
    font=nib.Font.TITLE,            # Typography
    foreground_color=nib.Color.BLUE, # Appearance
    padding=16,                      # Layout
    shadow_radius=4,                 # Effects
    animation=nib.Animation.spring(),# Animation
)
```

## Complete Modifier Table

### Layout

| Parameter | Type | Default | Description | Details |
|-----------|------|---------|-------------|---------|
| `width` | `float` | `None` | Fixed width in points. | [Layout](layout.md) |
| `height` | `float` | `None` | Fixed height in points. | [Layout](layout.md) |
| `min_width` | `float` | `None` | Minimum width in points. | [Layout](layout.md) |
| `min_height` | `float` | `None` | Minimum height in points. | [Layout](layout.md) |
| `max_width` | `float \| str` | `None` | Maximum width in points, or `"infinity"`. | [Layout](layout.md) |
| `max_height` | `float \| str` | `None` | Maximum height in points, or `"infinity"`. | [Layout](layout.md) |
| `padding` | `float \| dict` | `None` | Inner spacing (inside background). | [Layout](layout.md) |
| `margin` | `float \| dict` | `None` | Outer spacing (outside background). | [Layout](layout.md) |

### Appearance

| Parameter | Type | Default | Description | Details |
|-----------|------|---------|-------------|---------|
| `foreground_color` | `Color \| str` | `None` | Text and content color. | [Appearance](appearance.md) |
| `background` | `Color \| str \| View` | `None` | Background color or view. | [Appearance](appearance.md) |
| `fill` | `Color \| str` | `None` | Shape fill color. | [Appearance](appearance.md) |
| `stroke` | `Color \| str` | `None` | Shape stroke color. | [Appearance](appearance.md) |
| `stroke_width` | `float` | `None` | Shape stroke thickness. | [Appearance](appearance.md) |
| `opacity` | `float` | `None` | View transparency (0.0--1.0). | [Appearance](appearance.md) |
| `corner_radius` | `float \| CornerRadius` | `None` | Rounded corners in points. | [Appearance](appearance.md) |
| `clip_shape` | `str \| View` | `None` | Clip view to shape. | [Appearance](appearance.md) |
| `visible` | `bool` | `True` | Show or hide view entirely. | [Appearance](appearance.md) |

### Typography

| Parameter | Type | Default | Description | Details |
|-----------|------|---------|-------------|---------|
| `font` | `Font \| str` | `None` | Font configuration. | [Typography](typography.md) |
| `font_weight` | `FontWeight \| str` | `None` | Text weight. | [Typography](typography.md) |

### Effects

| Parameter | Type | Default | Description | Details |
|-----------|------|---------|-------------|---------|
| `shadow_color` | `Color \| str` | `None` | Drop shadow color. | [Effects](effects.md) |
| `shadow_radius` | `float` | `None` | Drop shadow blur radius. | [Effects](effects.md) |
| `shadow_x` | `float` | `None` | Drop shadow horizontal offset. | [Effects](effects.md) |
| `shadow_y` | `float` | `None` | Drop shadow vertical offset. | [Effects](effects.md) |
| `border_color` | `Color \| str` | `None` | Border color. | [Effects](effects.md) |
| `border_width` | `float` | `None` | Border width in points. | [Effects](effects.md) |
| `blend_mode` | `BlendMode \| str` | `None` | Layer blending mode. | [Effects](effects.md) |
| `scale` | `float` | `None` | Scale transform factor. | [Effects](effects.md) |
| `offset` | `Offset` | `None` | Position offset (x, y). | [Effects](effects.md) |
| `animation` | `Animation` | `None` | Animation for property changes. | [Effects](effects.md) |
| `content_transition` | `ContentTransition \| str` | `None` | How content changes animate. | [Effects](effects.md) |
| `transition` | `Transition \| str \| TransitionConfig` | `None` | How view appears/disappears. | [Effects](effects.md) |

### Interaction

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `on_drop` | `Callable[[list[str]], None]` | `None` | Callback for drag-and-drop file handling. |
| `on_hover` | `Callable[[bool], None]` | `None` | Callback when mouse enters/exits the view. |
| `on_click` | `Callable[[], None]` | `None` | Callback when the view is clicked. |
| `tooltip` | `str \| View` | `None` | Tooltip text shown on hover. |
| `overlay` | `View` | `None` | View rendered on top of this view. |
| `context_menu` | `list[View]` | `None` | Right-click context menu items. Accepts `Button`, `Toggle`, `Picker`, `Divider`, `Text`, `ShareLink`. See [Context Menu guide](../../guides/context-menu.md#view-context-menu). |
