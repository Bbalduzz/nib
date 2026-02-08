# SFSymbol

A view that displays an Apple SF Symbol icon. SF Symbols are a library of over 5,000 configurable icons designed for Apple platforms. `SFSymbol` inherits from `View`, so it supports all standard view modifiers.

Browse available symbols at [developer.apple.com/sf-symbols](https://developer.apple.com/sf-symbols/) or using the SF Symbols app.

## Constructor

```python
nib.SFSymbol(
    name,
    weight=None,
    scale=None,
    rendering_mode=None,
    # View modifiers
    width=None,
    height=None,
    padding=None,
    foreground_color=None,
    background=None,
    opacity=None,
    font=None,
    font_weight=None,
    **kwargs,
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | -- | SF Symbol name, e.g. `"star.fill"`, `"gear"`, `"heart.circle"` |
| `weight` | `str \| None` | `None` | Symbol weight. One of `"ultralight"`, `"thin"`, `"light"`, `"regular"`, `"medium"`, `"semibold"`, `"bold"`, `"heavy"`, `"black"` |
| `scale` | `str \| None` | `None` | Symbol scale. One of `"small"`, `"medium"`, `"large"` |
| `rendering_mode` | `SymbolRenderingMode \| str \| None` | `None` | How colors are applied to the symbol. One of `"monochrome"`, `"hierarchical"`, `"palette"`, `"multicolor"` |

In addition to the parameters above, `SFSymbol` accepts all standard `View` modifiers as keyword arguments:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `float \| None` | `None` | Fixed width in points |
| `height` | `float \| None` | `None` | Fixed height in points |
| `padding` | `float \| dict \| None` | `None` | Padding around the symbol. Float for uniform, or dict with keys like `"top"`, `"bottom"`, `"horizontal"`, `"vertical"` |
| `foreground_color` | `str \| Color \| None` | `None` | Symbol color. Accepts a color name, hex string, or `Color` instance |
| `background` | `str \| Color \| None` | `None` | Background color |
| `opacity` | `float \| None` | `None` | Opacity from 0.0 (transparent) to 1.0 (opaque) |
| `font` | `Font \| None` | `None` | Font that influences the symbol's size |
| `font_weight` | `str \| FontWeight \| None` | `None` | Alternative way to set symbol weight |

## Properties

| Property | Type | Description |
|---|---|---|
| `name` | `str` | The SF Symbol name. Readable and writable |

## Usage Contexts

`SFSymbol` can be used in several contexts:

- **Menu bar icon**: `app.icon = nib.SFSymbol("star.fill")`
- **Inside views**: As a child of any layout container
- **Button content**: `nib.Button(content=nib.SFSymbol("plus"), action=add)`
- **Menu item icon**: `nib.MenuItem("Settings", icon="gear")` (pass a string directly)

## Examples

### Basic icon in a layout

```python
import nib

def main(app: nib.App):
    app.icon = nib.SFSymbol("star.fill")
    app.width = 300
    app.height = 100

    app.build(
        nib.HStack(
            controls=[
                nib.SFSymbol("heart.fill", foreground_color=nib.Color.RED),
                nib.Text("Favorites"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Styled symbol with weight, scale, and rendering mode

```python
import nib

def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "cloud.sun.rain.fill",
        rendering_mode="multicolor",
    )
    app.width = 300
    app.height = 200

    app.build(
        nib.VStack(
            controls=[
                nib.SFSymbol(
                    "cloud.sun.rain.fill",
                    weight="bold",
                    scale="large",
                    rendering_mode=nib.SymbolRenderingMode.MULTICOLOR,
                    font=nib.Font.system(48),
                ),
                nib.Text("Weather", font=nib.Font.HEADLINE),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Icon button row

```python
import nib

def main(app: nib.App):
    app.icon = nib.SFSymbol("square.grid.2x2")
    app.width = 300
    app.height = 80

    def action(name):
        print(f"Tapped {name}")

    app.build(
        nib.HStack(
            controls=[
                nib.Button(
                    content=nib.SFSymbol("square.and.arrow.up"),
                    action=lambda: action("share"),
                ),
                nib.Button(
                    content=nib.SFSymbol("doc.on.doc"),
                    action=lambda: action("copy"),
                ),
                nib.Button(
                    content=nib.SFSymbol("trash", foreground_color=nib.Color.RED),
                    action=lambda: action("delete"),
                ),
            ],
            spacing=16,
            padding=20,
        )
    )

nib.run(main)
```

## Related

- [App](app.md) -- Uses `SFSymbol` for the `icon` property
- [MenuItem](menu.md) -- Accepts SF Symbol name strings for the `icon` parameter
