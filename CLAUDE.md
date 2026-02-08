# Nib

A Python framework for building native macOS menu bar applications using SwiftUI.

## Architecture

Two processes, one socket. Python owns the logic, Swift owns the screen. They communicate over a Unix socket using MessagePack. In dev mode Python spawns Swift; in a built `.app` Swift spawns Python.

- `render` — full view tree, sent once at startup
- `patch` — only what changed, sent on every update
- `event` — user interaction (tap, change, hover), sent from Swift to Python

See `architecture.md` for a detailed overview.

## Project Structure

```
nib/
├── sdk/python/nib/           # Python SDK
│   ├── core/
│   │   ├── app.py            # App class, SFSymbol, MenuItem, run()
│   │   ├── connection.py     # Unix socket client, MessagePack
│   │   ├── diff.py           # View tree diffing, patch generation
│   │   ├── settings.py       # Settings with UserDefaults persistence
│   │   ├── user_defaults.py  # Low-level UserDefaults access
│   │   ├── state.py          # Reactive State and Binding
│   │   ├── logging.py        # Logger with progress bar support
│   │   └── file_picker.py   # Open/save file dialogs
│   ├── views/
│   │   ├── controls/         # Text, Button, TextField, Toggle, Slider, Picker,
│   │   │                     # DatePicker, ColorPicker, Image, Video, Label, Link,
│   │   │                     # ProgressView, Gauge, Markdown, Table, SecureField,
│   │   │                     # TextEditor, Map, WebView, ShareLink, CameraPreview
│   │   ├── layout/           # VStack, HStack, ZStack, ScrollView, List, Section,
│   │   │                     # Form, Spacer, Divider, Group, NavigationStack,
│   │   │                     # NavigationLink, DisclosureGroup, Grid, LazyVGrid, LazyHGrid
│   │   ├── shapes/           # Rectangle, Circle, Ellipse, Capsule
│   │   ├── charts/           # Chart, LineMark, BarMark, AreaMark, PointMark,
│   │   │                     # RuleMark, RectMark, SectorMark
│   │   ├── effects/          # VisualEffectBlur
│   │   ├── canvas.py         # Canvas (Core Graphics drawing)
│   │   └── settings_page.py  # SettingsPage, SettingsTab
│   ├── cli/
│   │   ├── build.py          # nib build — .app bundling, compilation, signing
│   │   ├── run.py            # nib run — dev mode with hot reload
│   │   ├── create.py         # nib create — project scaffolding
│   │   └── obfuscate.py      # Bytecode obfuscation
│   ├── services/             # Battery, Connectivity, Screen, Keychain, Camera, LaunchAtLogin
│   ├── notifications/        # Notification, NotificationManager, scheduling, actions
│   ├── draw/                 # Canvas drawing primitives
│   ├── modifiers/            # Layout, appearance, typography, effects
│   └── types.py              # Color, Font, Animation, TextStyle, enums
│
├── package/Nib/              # Swift runtime
│   ├── App/
│   │   ├── AppDelegate.swift       # Entry point, message routing, bundled mode
│   │   ├── Handlers/               # ClipboardHandler, FileDialogHandler, UserDefaultsHandler
│   │   ├── Managers/               # HotkeyManager
│   │   └── Services/               # Battery, Camera, Connectivity, Keychain,
│   │                               # LaunchAtLogin, Notification, Screen
│   ├── Core/
│   │   ├── Plugins/                # PluginLoader, PluginProtocol
│   │   └── Registries/             # ViewBuilderRegistry, ModifierRegistry
│   ├── Network/
│   │   └── SocketServer.swift      # Unix socket server, MessagePack parsing
│   ├── Protocol/
│   │   ├── NibMessage.swift        # Message types
│   │   ├── ViewNode.swift          # View tree structure
│   │   ├── ViewModifier.swift      # Modifier types
│   │   ├── ViewProps.swift         # View property definitions
│   │   ├── DrawCommand.swift       # Canvas drawing commands
│   │   └── Types/                  # ChartTypes, LayoutTypes, MapTypes, etc.
│   └── UI/
│       ├── StatusBarController.swift       # Menu bar icon, popover, context menu
│       ├── SettingsWindowController.swift  # Settings window
│       ├── ViewStore.swift                 # Observable state for SwiftUI
│       ├── FontManager.swift               # Font loading
│       └── Rendering/
│           ├── DynamicView.swift     # Main SwiftUI renderer
│           ├── Builders/             # 18 builder files (per view type)
│           └── Modifiers/            # Appearance, layout, animation, transition, font
│
└── examples/
```

## Building

### Swift Runtime

```bash
cd package && swift build -c release
```

Binary: `package/.build/release/nib-runtime`

### Using Makefile

```bash
make build-runtime  # Build and copy runtime to SDK
make install        # Build and install in dev mode
```

## CLI

```bash
nib create myapp        # Scaffold a new project
nib run main.py         # Dev mode with hot reload (-r for recursive watch)
nib build main.py       # Build standalone .app bundle
nib build --native      # Compile to native .so via Cython
nib build --obfuscate   # Strip debug info from .pyc
nib build --no-compile  # Keep .py source files
```

Build config can go in `pyproject.toml` under `[tool.nib]` and `[tool.nib.build]`.

## API

### Function-based (recommended)

```python
import nib

def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star.fill")
    app.width = 300
    app.height = 400

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

### Key Concepts

**Views** — All UI elements inherit from `View`. Styling via constructor params:

```python
nib.Text("Hello", font=nib.Font.TITLE, foreground_color=nib.Color.BLUE, padding=16)
```

**Layouts** — Use `controls=` for children:

```python
nib.VStack(controls=[...], spacing=8)
nib.HStack(controls=[...], alignment=nib.VerticalAlignment.TOP)
```

**Reactivity** — Mutate view properties to trigger re-renders:

```python
text.content = "Updated"  # Triggers diff + patch
```

**Settings** — Persistent settings with UserDefaults:

```python
settings = nib.Settings({"dark_mode": False, "volume": 50})
app.register_settings(settings)
settings.dark_mode = True  # Persists in background
```

**Context menu** — Right-click on status bar icon:

```python
app.menu = [
    nib.MenuItem("Settings", action=open_settings, icon="gear"),
    nib.MenuDivider(),
    nib.MenuItem("Quit", action=app.quit),
]
```

**Notifications** — `app.notify("Title", "Body")`
**Hotkeys** — `app.on_hotkey("cmd+shift+n", callback)`
**Clipboard** — `app.clipboard = "text"` / `app.get_clipboard(callback)`
**File dialogs** — `app.open_file_dialog(callback=..., types=["txt"])` / `app.save_file_dialog(...)`
**Drag & drop** — `nib.VStack(controls=[...], on_drop=callback)`

## Modifiers (constructor params)

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

## Adding New Features

### New View Type

1. **Python**: Create class in `sdk/python/nib/views/` inheriting from `View`
2. **Swift**: Add case to `ViewNode.ViewType` enum
3. **Swift**: Add builder in `Rendering/Builders/`

### New Modifier

1. **Python**: Add parameter to `View.__init__` and `_apply_modifiers`
2. **Swift**: Add to `ViewNode.ViewModifier.ModifierType`
3. **Swift**: Add applier in `Rendering/Modifiers/`

### New Message Type

1. **Python**: Add method to `Connection` class
2. **Swift**: Add case to `NibMessage` enum
3. **Swift**: Handle in `SocketServer.parseMessage`
4. **Swift**: Process in `AppDelegate.handleMessage`

### New System Service

1. **Swift**: Create service in `App/Services/`
2. **Swift**: Wire in `AppDelegate` message handler
3. **Python**: Create module in `sdk/python/nib/services/`

## Swift Compilation Performance

The Swift type checker can get stuck on certain patterns. Avoid:

- Repeated conditional `AnyView` wrapping (causes type explosion)
- Recursive generic `@ViewBuilder` functions

Use `AnyView` only for truly dynamic iteration. For conditional modifiers, use separate `@ViewBuilder` helpers.

## Debugging

Swift runtime logs to `/tmp/nib.log`. Use `debugPrint()` in Swift code.
Python prints connection/render info to stdout.
