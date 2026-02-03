# Nib

Build native macOS menu bar apps in Python.

Write your app logic in Python with a declarative, SwiftUI-inspired API. Nib compiles to a native macOS app with real SwiftUI rendering—no Electron, no web views.

## Example

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("number.circle.fill")

    count = nib.Text("0", font=nib.Font.LARGE_TITLE)

    app.build(
        nib.VStack([
            count,
            nib.Button("Add", action=lambda: setattr(count, "content", str(int(count.content) + 1))),
        ], spacing=12, padding=20)
    )

nib.run(main)
```

## Why Nib?

- **Native performance** — Real SwiftUI rendering, smooth 60fps animations
- **Pythonic API** — Declarative syntax that feels natural, not a Swift wrapper
- **Reactive updates** — Change a property, UI updates automatically
- **Full system access** — Notifications, hotkeys, clipboard, file dialogs, drag & drop
- **Build & distribute** — Compile to a standalone `.app` bundle with `nib build`

## How It Works

```
┌─────────────────┐                        ┌─────────────────┐
│   Python App    │   Unix Socket + MsgPack│  Swift Runtime  │
│                 │ ◄─────────────────────►│                 │
│  Your code      │                        │  SwiftUI        │
│  View tree      │        render ───────► │  Status bar     │
│  Event handlers │ ◄─────── events        │  Native APIs    │
└─────────────────┘                        └─────────────────┘
```

Your Python code defines the UI as a tree of views. Nib serializes this tree and sends it to a Swift runtime process that renders native SwiftUI. User interactions flow back as events, triggering your Python callbacks.

The result: you write Python, users see a native Mac app.

## Features

**UI Components** — Text, Button, TextField, Toggle, Slider, Picker, Image, List, ScrollView, Charts, and more

**Layout** — VStack, HStack, ZStack, Spacer, Divider, Form, Section, NavigationStack

**Styling** — Colors, gradients, shadows, animations, SF Symbols, custom fonts

**System Integration** — macOS notifications, global keyboard shortcuts, clipboard access, file/save dialogs, drag & drop

**Settings** — Built-in settings window with tabs, auto-persistence to UserDefaults

**Context Menu** — Right-click menu on the status bar icon with nested items, shortcuts, badges

## Installation

**Requirements:** macOS 14+, Python 3.10+

```bash
pip install nib
```

Or build from source:

```bash
git clone https://github.com/nicebyte/nib.git
cd nib
make install
```

## Quick Start

```bash
# Create a new project
nib create myapp
cd myapp

# Run in development mode (hot reload)
nib run main.py

# Build a distributable .app
nib build
```

## License

MIT
