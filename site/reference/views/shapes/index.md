# Shapes

Shape views draw geometric forms that can be used as standalone content, backgrounds, overlays, or clip masks. All shapes inherit from `View` and accept common modifiers such as `width`, `height`, `padding`, `background`, `foreground_color`, `opacity`, `corner_radius`, `font`, `animation`, and more as constructor parameters.

## Built-in Shapes

| View | Description |
|------|-------------|
| [Rectangle](rectangle.md) | A rectangular shape with optional corner rounding, including per-corner radius control. |
| [Circle](circle.md) | A circular shape that maintains a 1:1 aspect ratio, with optional trim for progress rings. |
| [Ellipse](ellipse.md) | An oval shape that stretches to fill its frame with independent width and height. |
| [Capsule](capsule.md) | A pill-shaped rectangle where the shorter dimension is completely rounded. |

## Custom Shapes

| View | Description |
|------|-------------|
| [Path & Shape](path.md) | Build custom shapes using path operations: lines, curves, arcs, and geometric primitives. |

## Gradients

| View | Description |
|------|-------------|
| [Gradients](gradients.md) | Color gradients including linear, radial, angular, and elliptical variations. |

## Common Shape Parameters

All built-in shapes accept these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `fill` | `str \| Color` | Fill color for the shape interior. Accepts hex strings (`"#FF5733"`), named colors (`"red"`), or `Color` instances. |
| `stroke_color` | `str \| Color` | Stroke color for the shape border. |
| `stroke_width` | `float` | Width of the stroke in points. |

Shapes are commonly used in three patterns:

- **Standalone** -- as visible UI elements with explicit dimensions
- **Background** -- passed to the `background` modifier of another view
- **Clip shape** -- passed to the `clip_shape` modifier to mask content
