# VisualEffectBlur

A view that applies a macOS frosted-glass blur effect, wrapping `NSVisualEffectView`. It creates the translucent blur commonly seen in menu bar apps, sidebars, and other system UI. Can be used as a standalone view or as a background for other views.

All properties are reactive -- updating them triggers an immediate UI refresh.

## Constructor

```python
nib.VisualEffectBlur(
    material=BlurStyle.POPOVER,
    blending_mode=BlurBlendingMode.BEHIND_WINDOW,
    is_emphasized=False,
    corner_radius=None,
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `material` | `BlurStyle` | `BlurStyle.POPOVER` | The blur material/style. Controls the visual appearance and vibrancy level. See the BlurStyle table below. |
| `blending_mode` | `BlurBlendingMode` | `BlurBlendingMode.BEHIND_WINDOW` | How the blur blends with content. `BEHIND_WINDOW` blurs content behind the window; `WITHIN_WINDOW` blurs content within the same window. |
| `is_emphasized` | `bool` | `False` | Whether to use the emphasized appearance, which increases vibrancy. |
| `corner_radius` | `float` | `None` | Corner radius for a rounded blur region. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `opacity`, etc. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `material` | `BlurStyle` | Get or set the blur material. Setting triggers a UI update. |
| `blending_mode` | `BlurBlendingMode` | Get or set the blending mode. |
| `is_emphasized` | `bool` | Get or set the emphasized state. |
| `corner_radius` | `float \| None` | Get or set the corner radius. |

## BlurStyle

The `BlurStyle` enum maps to `NSVisualEffectView.Material` values on macOS.

### Standard materials

| Value | Description |
|-------|-------------|
| `HEADER_VIEW` | Header region style. |
| `TOOLTIP` | Tooltip popup style. |
| `MENU` | Menu background style. |
| `POPOVER` | Popover background style. Default. |
| `SIDEBAR` | Sidebar panel style. |
| `FULLSCREEN_UI` | Full-screen overlay style. |
| `HUD` | Heads-up display style. |
| `SHEET` | Sheet overlay style. |
| `WINDOW_BACKGROUND` | Window background style. |
| `CONTENT_BACKGROUND` | Content area background. |
| `UNDER_WINDOW_BACKGROUND` | Under-window background. |
| `UNDER_PAGE_BACKGROUND` | Under-page background. |

### Vibrancy

| Value | Description |
|-------|-------------|
| `TITLEBAR` | Title bar vibrancy. |
| `SELECTION` | Selection highlight vibrancy. |

### System materials

| Value | Description |
|-------|-------------|
| `ULTRA_THIN` | Ultra-thin blur. Most transparent. |
| `THIN` | Thin blur. |
| `REGULAR` | Regular blur. |
| `THICK` | Thick blur. |
| `ULTRA_THICK` | Ultra-thick blur. Most opaque. |

## BlurBlendingMode

| Value | Description |
|-------|-------------|
| `BEHIND_WINDOW` | Blurs content behind the entire window. |
| `WITHIN_WINDOW` | Blurs content within the same window, behind this view. |

## Examples

### As a view background

```python
import nib

def main(app: nib.App):
    app.build(
        nib.ZStack(controls=[
            nib.VisualEffectBlur(material=nib.BlurStyle.POPOVER),
            nib.VStack(
                controls=[
                    nib.Text("Blurred Background", font=nib.Font.TITLE),
                    nib.Text("Content rendered over frosted glass"),
                ],
                spacing=8,
                padding=20,
            ),
        ])
    )

nib.run(main)
```

### Menu-style blur with rounded corners

```python
import nib

blur = nib.VisualEffectBlur(
    material=nib.BlurStyle.MENU,
    corner_radius=10,
    width=300,
    height=200,
)
```

### Sidebar style

```python
import nib

sidebar_blur = nib.VisualEffectBlur(
    material=nib.BlurStyle.SIDEBAR,
    blending_mode=nib.BlurBlendingMode.BEHIND_WINDOW,
    width=250,
)
```

### Updating material reactively

```python
import nib

def main(app: nib.App):
    blur = nib.VisualEffectBlur(
        material=nib.BlurStyle.THIN,
        width=300,
        height=200,
    )

    def toggle_thickness():
        if blur.material == nib.BlurStyle.THIN:
            blur.material = nib.BlurStyle.ULTRA_THICK
        else:
            blur.material = nib.BlurStyle.THIN

    app.build(
        nib.VStack(controls=[
            blur,
            nib.Button("Toggle Blur", action=toggle_thickness),
        ], spacing=12, padding=16)
    )

nib.run(main)
```
