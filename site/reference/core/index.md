# Core API Reference

The core module contains the foundational classes and functions for building Nib menu bar applications.

## Entry Point

| Class / Function | Description |
|---|---|
| [App](app.md) | Main application class that manages the lifecycle of a menu bar app |
| [run()](run.md) | Recommended entry point for function-based apps |

## UI Primitives

| Class / Function | Description |
|---|---|
| [SFSymbol](sfsymbol.md) | Displays Apple SF Symbol icons in the menu bar or views |
| [MenuItem & MenuDivider](menu.md) | Items for the right-click context menu on the status bar icon |

## State Management

| Class / Function | Description |
|---|---|
| [State & Binding](state.md) | Reactive state descriptor and two-way data binding for class-based apps |
| [Settings](settings.md) | Persistent settings with sync cache and async UserDefaults persistence |
| [UserDefaults](user-defaults.md) | Low-level persistent key-value storage using macOS UserDefaults |

## UI Configuration

| Class / Function | Description |
|---|---|
| [SettingsPage & SettingsTab](settings-page.md) | Tabbed preferences window following macOS conventions |
| [FilePicker](file-picker.md) | Native macOS open/save file dialogs |

## Quick Example

```python
import nib

def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star.fill")
    app.width = 300
    app.height = 200

    counter = nib.Text("0")

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
