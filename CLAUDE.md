# Nib

A Python framework for building native macOS menu bar applications using SwiftUI.

## Overview

Nib lets you write macOS menu bar apps in Python with a declarative, SwiftUI-inspired API. Python code communicates with a Swift runtime over Unix sockets using MessagePack serialization.

## Architecture

```
┌─────────────────┐     Unix Socket      ┌─────────────────┐
│   Python App    │ ←───────────────────→│  Swift Runtime  │
│                 │     (MessagePack)    │                 │
│  - View tree    │                      │  - Status bar   │
│  - Event logic  │                      │  - SwiftUI      │
│  - State        │                      │  - Notifications│
└─────────────────┘                      └─────────────────┘
```

### Communication Protocol

**Python → Swift messages:**
- `render` - Full UI tree (initial render or major changes)
- `patch` - Incremental updates (props, modifiers, insert, remove)
- `notify` - System notifications
- `quit` - Shutdown

**Swift → Python messages:**
- `event` - User interactions (tap, change:value)

## Project Structure

```
nib/
├── sdk/python/nib/       # Python SDK
│   ├── core/
│   │   ├── app.py        # App class, SFSymbol, run()
│   │   ├── connection.py # Unix socket client, MessagePack
│   │   └── diff.py       # View tree diffing
│   ├── views/
│   │   ├── base.py       # Base View class with modifiers
│   │   ├── controls/     # Button, Text, TextField, Toggle, etc.
│   │   ├── layout/       # VStack, HStack, ZStack, ScrollView, etc.
│   │   └── shapes/       # Rectangle, Circle, Capsule, etc.
│   └── types.py          # Color, Font, Animation, etc.
│
├── package/Nib/          # Swift runtime (nib-runtime)
│   ├── App/
│   │   └── AppDelegate.swift    # Entry point, message routing
│   ├── Network/
│   │   └── SocketServer.swift   # Unix socket server
│   ├── Protocol/
│   │   ├── NibMessage.swift     # Message types
│   │   └── ViewNode.swift       # View tree structure
│   └── UI/
│       ├── StatusBarController.swift  # Menu bar integration
│       ├── ViewStore.swift            # Observable state
│       └── Rendering/
│           ├── DynamicView.swift      # SwiftUI renderer
│           ├── Builders/              # View builders
│           └── Modifiers/             # Modifier appliers
│
└── examples/             # Example apps
    ├── showcase.py       # Feature showcase
    ├── yt_downloader.py  # YouTube downloader
    └── didyouknow.py     # Music info popover
```

## Building

### Swift Runtime

```bash
cd package
swift build -c release
```

The binary is at `package/.build/release/nib-runtime`.

### Using Makefile

```bash
make build-runtime  # Build and copy runtime to SDK
make install        # Build and install in dev mode
```

### Python SDK

No build step required. Just ensure the Swift runtime is built.

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

### Key Concepts

**Views** - All UI elements inherit from `View`. Styling via constructor params (no method chaining):

```python
nib.Text(
    "Hello",
    font=nib.Font.title,
    foreground_color=nib.Color.blue,
    padding=16,
)
```

**Layouts** - Use `controls=` parameter for children:

```python
nib.VStack(controls=[...], spacing=8)
nib.HStack(controls=[...], alignment=nib.VerticalAlignment.top)
nib.ZStack(controls=[...])
```

**Reactivity** - Mutate view properties to trigger re-renders:

```python
text = nib.Text("Hello")
text.content = "World"  # Triggers re-render

field = nib.TextField(value="")
field.value = "new value"  # Triggers re-render
```

**Background views** - Any view can be a background:

```python
nib.VStack(
    controls=[...],
    background=nib.RoundedRectangle(
        corner_radius=10,
        fill="#262626",
        stroke_color="#383837",
        stroke_width=1,
    ),
)
```

**Overlay views** - Any view can be an overlay (rendered on top):

```python
nib.VStack(
    controls=[...],
    overlay=nib.Circle(
        stroke="#FF0000",
        stroke_width=2,
    ),
)
```

**Notifications** - macOS system notifications:

```python
app.notify("Title", "Body text")
app.notify(
    title="Download Complete",
    body="File saved",
    subtitle="Downloader",
    sound=True,
)
```

**Right-click menu** - Menu bar context menu:

```python
app.menu = [
    nib.MenuItem("Settings", action=open_settings, icon="gear"),
    nib.MenuItem("Check for Updates", action=check_updates),
    nib.MenuDivider(),
    nib.MenuItem("Quit", action=app.quit),
]
```

**Keyboard shortcuts** - Global hotkeys:

```python
app.on_hotkey("cmd+shift+n", show_window)

@app.hotkey("cmd+k")
def quick_action():
    pass
```

**Clipboard** - Read/write system clipboard:

```python
app.clipboard = "Hello World"  # Write

app.get_clipboard(lambda text: print(f"Clipboard: {text}"))  # Async read
```

**File dialogs** - Open/save file pickers:

```python
def on_files(paths: list[str]):
    print(f"Selected: {paths}")

app.open_file_dialog(
    callback=on_files,
    title="Select files",
    types=["txt", "md"],
    multiple=True,
)

app.save_file_dialog(
    callback=lambda path: print(f"Save to: {path}"),
    title="Save as",
    default_name="untitled.txt",
)
```

**Drag and drop** - Accept dropped files on views:

```python
def on_drop(files: list[str]):
    print(f"Dropped: {files}")

nib.VStack(
    controls=[...],
    on_drop=on_drop,
)
```

## Available Views

### Layout
- `VStack`, `HStack`, `ZStack`
- `ScrollView`, `List`, `Section`
- `Spacer`, `Divider`, `Group`
- `NavigationStack`, `NavigationLink`, `DisclosureGroup`

### Controls
- `Text`, `TextField`, `SecureField`
- `Button`, `Toggle`, `Slider`, `Stepper`
- `Picker`, `DatePicker`, `ColorPicker`
- `Image`, `Label`, `Link`
- `ProgressView`

### Shapes
- `Rectangle`, `RoundedRectangle`
- `Circle`, `Ellipse`, `Capsule`

### Special
- `SFSymbol` - Apple SF Symbols with weight, scale, rendering mode

## Modifiers (constructor params)

All views support these modifiers:

```python
# Layout
width, height, min_width, min_height, max_width, max_height
padding  # float or dict with top/bottom/leading/trailing/horizontal/vertical

# Appearance
background  # Color or View
foreground_color
fill, stroke, stroke_width  # For shapes
opacity
corner_radius
clip_shape  # "capsule", "circle", or shape View

# Shadow
shadow_color, shadow_radius, shadow_x, shadow_y

# Border
border_color, border_width

# Typography
font  # Font.title, Font.system(size, weight), etc.
font_weight

# Animation
animation  # Animation.spring(), Animation.easeInOut(0.3), etc.
content_transition, transition

# Transform
scale, blend_mode
```

## View IDs

Views get position-based IDs during render (e.g., "0", "0.1", "0.1.2"). These are used for:
- Event routing (tap, change)
- Incremental updates (patching)

## Adding New Features

### New View Type

1. **Python**: Create class in `sdk/python/nib/views/` inheriting from `View`
2. **Swift**: Add case to `ViewNode.ViewType` enum
3. **Swift**: Add builder in `DynamicView` or `Builders/`

### New Modifier

1. **Python**: Add parameter to `View.__init__` and `_apply_modifiers`
2. **Swift**: Add to `ViewNode.ViewModifier.ModifierType`
3. **Swift**: Add applier in `Modifiers/`

### New Message Type

1. **Python**: Add method to `Connection` class
2. **Swift**: Add case to `NibMessage` enum
3. **Swift**: Handle in `SocketServer.parseMessage`
4. **Swift**: Process in `AppDelegate.handleMessage`

## Swift Compilation Performance

The Swift type checker can get stuck for hours on certain code patterns. Avoid these:

### Patterns to Avoid

**1. Repeated `AnyView` wrapping in a loop:**
```swift
// BAD - exponential type complexity
var view = AnyView(content)
if condition1 { view = AnyView(view.modifier1()) }
if condition2 { view = AnyView(view.modifier2()) }
```

**2. Recursive generic `@ViewBuilder` functions:**
```swift
// BAD - exponential nested types
@ViewBuilder
func apply<V: View>(to view: V, at index: Int) -> some View {
    apply(to: view.modifier(), at: index + 1)
}
```

### Correct Patterns

**For conditional modifiers, use separate `@ViewBuilder` helpers:**
```swift
// GOOD
content
    .applyModifier1(condition1)
    .applyModifier2(condition2)

@ViewBuilder
func applyModifier1(_ condition: Bool) -> some View {
    if condition { self.modifier1() } else { self }
}
```

**For dynamic modifier chains, use iterative `AnyView`:**
```swift
// GOOD - type erasure is appropriate here
var result = AnyView(content)
for modifier in modifiers {
    result = AnyView(result.apply(modifier))
}
```

The key insight: `AnyView` is bad when used conditionally in static code (causes type explosion), but fine for truly dynamic iteration where types can't be known at compile time.

## Running Examples

```bash
cd examples
python showcase.py
python yt_downloader.py
python didyouknow.py
```

## Debugging

Swift runtime logs to `/tmp/nib.log`. Use `debugPrint()` in Swift code.

Python prints connection/render info to stdout.
