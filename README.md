# Nib

A Python framework for building native macOS menu bar applications using SwiftUI.

Write your menu bar apps in Python with a declarative, SwiftUI-inspired API. Nib handles the native rendering, so you get smooth animations, system integration, and that polished macOS feel.

## Features

- **Declarative UI** - SwiftUI-inspired syntax that feels natural in Python
- **Native rendering** - Real SwiftUI under the hood, not web views
- **Reactive updates** - Change a property, UI updates automatically
- **System integration** - Notifications, file dialogs, clipboard, global hotkeys
- **Rich components** - Text, buttons, toggles, sliders, pickers, images, charts, and more
- **Flexible styling** - Gradients, shadows, animations, SF Symbols

## Quick Start

```python
import nib

def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star.fill")
    app.width = 300
    app.height = 200

    counter = nib.Text("0", font=nib.Font.largeTitle)

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.build(
        nib.VStack(
            controls=[
                counter,
                nib.Button("Add", action=increment),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

## Installation

### Requirements

- macOS 14.0+
- Python 3.10+
- Xcode Command Line Tools

### Build from source

```bash
# Clone the repository
git clone https://github.com/example/nib.git
cd nib

# Build the Swift runtime
cd swift
swift build -c release

# Run an example
cd ../examples
python showcase.py
```

## Documentation

### Views

**Layout**
```python
nib.VStack(controls=[...], spacing=8)      # Vertical stack
nib.HStack(controls=[...], spacing=8)      # Horizontal stack
nib.ZStack(controls=[...])                 # Overlay stack
nib.ScrollView([...])                      # Scrollable container
nib.List(controls=[...])                   # Native list
nib.Spacer()                               # Flexible space
```

**Controls**
```python
nib.Text("Hello", font=nib.Font.title)
nib.Button("Click", action=on_click)
nib.TextField(placeholder="Enter text", on_change=on_change)
nib.Toggle("Enable", value=True, on_change=on_toggle)
nib.Slider(value=0.5, on_change=on_slide)
nib.Picker(options=["A", "B", "C"], value="A", on_change=on_pick)
nib.Image(url="https://...")
nib.ProgressView(progress=0.7)
nib.Markdown("# Hello **World**")
```

**Shapes & Gradients**
```python
nib.RoundedRectangle(corner_radius=10, fill="#007AFF")
nib.Circle(width=50, height=50, fill=nib.Color.red)
nib.LinearGradient(colors=["#FF6B6B", "#4ECDC4"], start=(0, 0), end=(1, 1))
nib.RadialGradient(colors=["white", "black"], center=(0.5, 0.5))
```

### Styling

All views accept styling parameters:

```python
nib.Text(
    "Styled",
    font=nib.Font.title,
    foreground_color=nib.Color.blue,
    padding=16,
    background=nib.Color.gray.opacity(0.1),
    corner_radius=8,
    shadow_radius=4,
)
```

### Reactivity

Mutate view properties to trigger automatic UI updates:

```python
label = nib.Text("Loading...")
progress = nib.ProgressView()

def on_progress(value):
    label.content = f"{int(value * 100)}%"
    progress.progress = value
```

### System Features

**Notifications**
```python
app.notify("Download Complete", "Your file is ready")
```

**Global Hotkeys**
```python
@app.hotkey("cmd+shift+n")
def show_window():
    print("Hotkey pressed!")
```

**Clipboard**
```python
app.clipboard = "Copied text"
app.get_clipboard(lambda text: print(text))
```

**File Dialogs**
```python
app.open_file_dialog(
    callback=lambda paths: print(paths),
    types=["txt", "md"],
    multiple=True,
)
```

**Context Menu**
```python
app.menu = [
    nib.MenuItem("Settings", action=open_settings, icon="gear"),
    nib.MenuDivider(),
    nib.MenuItem("Quit", action=app.quit),
]
```

### Charts

```python
nib.Chart(
    marks=[
        nib.LineMark(x="date", y="value", data=timeseries),
        nib.PointMark(x="date", y="value", data=timeseries),
    ],
    width=300,
    height=200,
)
```

## Examples

The `examples/` directory contains several demo apps:

- `showcase.py` - Feature showcase with all components
- `timer.py` - Pomodoro timer with notifications
- `gradient_demo.py` - All gradient types
- `markdown_demo.py` - Markdown rendering
- `chart_demo.py` - Charts and data visualization

Run any example:

```bash
cd examples
python showcase.py
```

## Architecture

```
┌─────────────────┐     Unix Socket      ┌─────────────────┐
│   Python App    │ ←───────────────────→│  Swift Runtime  │
│                 │     (MessagePack)    │                 │
│  - View tree    │                      │  - Status bar   │
│  - Event logic  │                      │  - SwiftUI      │
│  - State        │                      │  - Native APIs  │
└─────────────────┘                      └─────────────────┘
```

Nib uses a client-server architecture:
- **Python** defines the UI tree and handles events
- **Swift runtime** renders native SwiftUI and sends events back
- Communication happens over Unix sockets with MessagePack serialization

## Project Structure

```
nib/
├── python/nib/          # Python package
│   ├── core/            # App, connection, diffing
│   ├── views/           # All view components
│   └── types.py         # Color, Font, Animation, etc.
├── swift/Nib/           # Swift runtime
│   ├── App/             # AppDelegate, entry point
│   ├── Protocol/        # Message types, ViewNode
│   └── UI/              # SwiftUI rendering
└── examples/            # Example applications
```

## Debugging

Swift runtime logs to `/tmp/nib.log`:

```bash
tail -f /tmp/nib.log
```

## License

MIT
