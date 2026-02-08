# Nib

**Build native macOS menu bar apps in Python.**

Nib is a Python framework that lets you create macOS menu bar applications with a declarative, SwiftUI-inspired API. Write your app logic in Python — Nib handles the native rendering through a Swift runtime.

![Nib demo](assets/img/nib-demo.apng)

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
            controls=[
                counter,
                nib.Button("Add", action=increment),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

## Why Nib?

- **Native SwiftUI rendering** — Your app looks and feels like a real macOS app because it is one. No web views, no Electron.
- **Python simplicity** — Write your entire app in Python. No Swift knowledge required.
- **30+ UI components** — Text, buttons, toggles, sliders, pickers, charts, maps, tables, canvas drawing, and more.
- **System integration** — Access battery, connectivity, screen, keychain, camera, notifications, and file dialogs.
- **Reactive updates** — Mutate a property and the UI updates automatically. No state management boilerplate.
- **Build to .app** — Bundle your app into a standalone `.app` with `nib build`. Includes Python runtime, dependencies, and code signing.
- **Hot reload** — `nib run` watches your files and reloads on every save.

## Quick Start

```bash
pip install pynib
nib create myapp
cd myapp
nib run src/main.py
```

## Requirements

- macOS 14+
- Python 3.10+

## Next Steps

- **[Getting Started](getting-started/index.md)** — Install Nib and build your first app in minutes.
- **[Concepts](concepts/index.md)** — Understand the architecture, reactivity model, and view system.
- **[Guides](guides/index.md)** — Task-oriented guides for layouts, styling, animations, notifications, and more.
- **[API Reference](reference/index.md)** — Complete reference for every class, method, and parameter.
