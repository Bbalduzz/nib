# Views Reference

Views are the building blocks of Nib user interfaces. Every visible element on screen is a view. All views inherit from a common `View` base class and accept constructor parameters for layout, appearance, typography, animation, and other modifiers.

Views are organized into the following categories:

| Category | Description |
|----------|-------------|
| [Controls](controls/index.md) | Interactive UI elements for displaying content and capturing input: Text, Button, TextField, Toggle, Slider, Picker, Image, Video, Table, Map, WebView, and more. |
| [Layout](layout/index.md) | Container views that arrange children: VStack, HStack, ZStack, ScrollView, List, Form, NavigationStack, Grid, and more. |
| [Shapes](shapes/index.md) | Geometric shape views: Rectangle, Circle, Ellipse, Capsule. |
| [Charts](charts/index.md) | Data visualization powered by Swift Charts: Chart, LineMark, BarMark, AreaMark, PointMark, RuleMark, RectMark, SectorMark. |
| [Effects](effects/index.md) | Visual effect views: VisualEffectBlur for macOS frosted-glass blur, and Canvas for freeform Core Graphics drawing. |

## Common modifiers

All views accept these constructor parameters for styling and layout:

```python
# Layout
width, height, min_width, min_height, max_width, max_height
padding  # float or dict: {"top": 8, "horizontal": 16}

# Appearance
background, foreground_color, fill, stroke, stroke_width
opacity, corner_radius, clip_shape

# Shadow & Border
shadow_color, shadow_radius, shadow_x, shadow_y
border_color, border_width

# Typography
font, font_weight

# Animation
animation, content_transition, transition

# Transform
scale, blend_mode
```
