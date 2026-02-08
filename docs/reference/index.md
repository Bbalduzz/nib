# API Reference

Complete reference for every class, function, and parameter in the Nib Python SDK. Each page documents the constructor, properties, methods, and includes working code examples.

## Sections

| Section | Description |
|---------|-------------|
| [Core](core/index.md) | Entry points, app lifecycle, menus, state management, settings, and file dialogs |
| [Views -- Controls](views/controls/index.md) | Interactive and display controls: Text, Button, TextField, Toggle, Slider, Image, and more |
| [Views -- Layout](views/layout/index.md) | Layout containers: VStack, HStack, ZStack, ScrollView, List, Grid, NavigationStack |
| [Views -- Shapes](views/shapes/index.md) | Shape primitives: Rectangle, Circle, Ellipse, Capsule, Path, and Gradients |
| [Views -- Charts](views/charts/index.md) | Swift Charts integration: Chart, LineMark, BarMark, AreaMark, SectorMark, and more |
| [Views -- Effects](views/effects/index.md) | Visual effects: VisualEffectBlur, Canvas |
| [Draw Module](draw/index.md) | Canvas drawing primitives, paint, gradients, path elements, and image/text rendering |
| [Types & Enums](types/index.md) | Color, Font, Animation, Transition, TextStyle, alignment and style enums |
| [Services](services/index.md) | System services: Battery, Connectivity, Screen, Keychain, Camera, LaunchAtLogin, Permissions |
| [Notifications](notifications/index.md) | macOS notification system: Notification, NotificationManager, sounds, and actions |
| [Modifiers](modifiers/index.md) | View modifiers for layout, appearance, typography, and effects |

## Quick Example

```python
import nib

def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star.fill")
    app.width = 300
    app.height = 200

    counter = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.build(
        nib.VStack(
            controls=[counter, nib.Button("Add", action=increment)],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
