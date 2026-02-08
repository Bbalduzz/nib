# Event Handling

Events flow from Swift to Python over the Unix socket. When a user taps a button, types in a text field, or drops a file, Swift sends an event message containing the view's node ID and the event data. Python looks up the registered callback and calls it.

## How Events Work

1. You register a callback when creating a view (e.g., `action=` on a Button, `on_change=` on a TextField).
2. During each render, `App._collect_actions()` walks the view tree and builds maps from node IDs to callback functions.
3. When the user interacts with the view, Swift sends an event message with the node ID and event string.
4. Python's event handler looks up the callback in the appropriate map and calls it.

Events are dispatched sequentially on a dedicated event thread. This prevents concurrent callback execution, so you do not need locks when modifying view properties inside event handlers.

## Button Actions

Buttons use the `action=` parameter. The callback receives no arguments.

```python
import nib

def main(app: nib.App):
    count = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        count.content = str(int(count.content) + 1)

    def reset():
        count.content = "0"

    app.build(
        nib.VStack(
            controls=[
                count,
                nib.HStack(
                    controls=[
                        nib.Button("Add", action=increment),
                        nib.Button("Reset", action=reset),
                    ],
                    spacing=8,
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

!!! note "Callback signature"
    Button action callbacks take no arguments: `def handler():`. The button does not pass any value -- it simply signals that it was tapped.

## Text Field Changes

`TextField` and `SecureField` use `on_change=` for value changes and `on_submit=` for the Return/Enter key. Both receive the current text value as a string.

```python
search_field = nib.TextField(
    placeholder="Search...",
    value="",
    on_change=handle_search,
    on_submit=submit_search,
    style=nib.TextFieldStyle.roundedBorder,
)

def handle_search(value: str):
    # Called on every keystroke
    print(f"Searching: {value}")

def submit_search(value: str):
    # Called when user presses Return/Enter
    print(f"Submitted: {value}")
```

Secure fields work the same way:

```python
password_field = nib.SecureField(
    placeholder="Password",
    value="",
    on_change=lambda pw: validate_password(pw),
    on_submit=lambda pw: login(pw),
)
```

## TextEditor Changes

`TextEditor` provides multi-line text input with `on_change=`:

```python
notes = nib.TextEditor(
    text="",
    placeholder="Enter your notes...",
    on_change=handle_notes_change,
)

def handle_notes_change(text: str):
    # Called when the text content changes
    word_count.content = f"{len(text.split())} words"
```

## Toggle Changes

`Toggle` uses `on_change=` and passes a boolean indicating the new state.

```python
dark_mode = nib.Toggle(
    "Dark Mode",
    is_on=False,
    on_change=handle_dark_mode,
)

def handle_dark_mode(is_on: bool):
    if is_on:
        container.background = "#1a1a1a"
        label.foreground_color = "#ffffff"
    else:
        container.background = "#ffffff"
        label.foreground_color = "#000000"
```

## Slider Changes

`Slider` uses `on_change=` and passes the new float value. The callback is called continuously while dragging.

```python
volume_label = nib.Text("Volume: 50%")

volume_slider = nib.Slider(
    value=50,
    min_value=0,
    max_value=100,
    step=1,
    on_change=handle_volume,
)

def handle_volume(value: float):
    volume_label.content = f"Volume: {int(value)}%"
```

## Picker Changes

`Picker` uses `on_change=` and passes the selected value as a string.

```python
nib.Picker(
    "Theme",
    selection="system",
    options=[
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ],
    on_change=handle_theme,
    style=nib.PickerStyle.segmented,
)

def handle_theme(value: str):
    print(f"Selected theme: {value}")  # "light", "dark", or "system"
```

## Lifecycle Events

The app provides lifecycle callbacks for the popover window and app termination.

```python
def main(app: nib.App):
    app.on_appear = on_open
    app.on_disappear = on_close
    app.on_quit = on_quit

    # ...

def on_open():
    # Called every time the popover opens (user clicks menu bar icon)
    print("Popover opened")
    refresh_data()

def on_close():
    # Called every time the popover closes
    print("Popover closed")
    pause_updates()

def on_quit():
    # Called once when the app is shutting down
    print("App quitting")
    save_state()
    close_connections()
```

| Event | When it fires | Frequency |
|---|---|---|
| `on_appear` | Popover opens | Every open |
| `on_disappear` | Popover closes | Every close |
| `on_quit` | App is shutting down | Once |

## Drag and Drop

Any container view can accept dropped files via `on_drop=`. The callback receives a list of file path strings.

```python
drop_zone = nib.VStack(
    controls=[
        nib.SFSymbol("arrow.down.doc", font=nib.Font.TITLE),
        nib.Text("Drop files here"),
    ],
    spacing=8,
    padding=24,
    border_color="#666666",
    border_width=1,
    corner_radius=8,
    on_drop=handle_drop,
)

def handle_drop(paths: list[str]):
    for path in paths:
        print(f"Received: {path}")
    status.content = f"Dropped {len(paths)} file(s)"
```

## Hover Events

Any view can detect mouse hover via `on_hover=`. The callback receives a boolean -- `True` when the mouse enters, `False` when it exits.

```python
card = nib.VStack(
    controls=[nib.Text("Hover me")],
    padding=16,
    background="#333333",
    corner_radius=8,
    on_hover=handle_hover,
    animation=nib.Animation.EASE_IN_OUT,
)

def handle_hover(is_hovering: bool):
    if is_hovering:
        card.background = "#444444"
        card.scale = 1.02
    else:
        card.background = "#333333"
        card.scale = 1.0
```

## Click Events

Any view can respond to clicks via `on_click=`. The callback receives no arguments.

```python
nib.VStack(
    controls=[
        nib.SFSymbol("checkmark.circle"),
        nib.Text("Click to select"),
    ],
    spacing=4,
    padding=12,
    on_click=lambda: print("Selected!"),
)
```

## Canvas Gestures

The `Canvas` view supports gesture tracking for drawing and interactive graphics. Enable gestures with `enable_gestures=True` or by setting any gesture callback.

Gesture callbacks receive a `PanEvent` with `x` and `y` coordinates in the canvas coordinate space.

```python
import nib

def main(app: nib.App):
    canvas = nib.Canvas(width=400, height=300, background_color="#1a1a1a")
    last_pos = None

    def on_pan_start(e: nib.PanEvent):
        nonlocal last_pos
        last_pos = (e.x, e.y)

    def on_pan_update(e: nib.PanEvent):
        nonlocal last_pos
        if last_pos:
            canvas.append(nib.draw.Line(
                x1=last_pos[0], y1=last_pos[1],
                x2=e.x, y2=e.y,
                stroke="#ffffff", stroke_width=3,
            ))
            last_pos = (e.x, e.y)

    def on_pan_end(e: nib.PanEvent):
        nonlocal last_pos
        last_pos = None

    def on_hover(e: nib.PanEvent):
        # Mouse is moving over canvas (not dragging)
        coords.content = f"({e.x:.0f}, {e.y:.0f})"

    canvas.on_pan_start = on_pan_start
    canvas.on_pan_update = on_pan_update
    canvas.on_pan_end = on_pan_end
    canvas.on_hover = on_hover

    coords = nib.Text("(0, 0)", font=nib.Font.CAPTION)

    app.build(
        nib.VStack(
            controls=[canvas, coords],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

| Callback | When it fires | Argument |
|---|---|---|
| `on_pan_start` | Mouse/pen pressed down | `PanEvent(x, y)` |
| `on_pan_update` | Mouse/pen dragged | `PanEvent(x, y)` |
| `on_pan_end` | Mouse/pen released | `PanEvent(x, y)` |
| `on_hover` | Mouse moves (not dragging) | `PanEvent(x, y)` |

!!! info "Canvas hover vs view hover"
    Canvas `on_hover` receives a `PanEvent` with x/y coordinates. View `on_hover` (on any other view) receives a `bool` indicating whether the mouse entered or exited. They share the same parameter name but have different callback signatures depending on the view type.

## Hotkeys

Register global keyboard shortcuts that work even when the app window is not focused.

```python
def main(app: nib.App):
    app.on_hotkey("cmd+shift+n", show_new_dialog)
    app.on_hotkey("cmd+k", toggle_search)

    # Decorator syntax
    @app.hotkey("cmd+shift+p")
    def open_command_palette():
        print("Command palette opened")
```

Hotkey strings use modifier names joined with `+`: `cmd`, `shift`, `opt` (or `alt`), `ctrl`, plus a key name.

## Context Menu Events

Right-click menu items use the `action=` parameter, same as buttons.

```python
app.menu = [
    nib.MenuItem("Settings", action=open_settings, icon="gear", shortcut="cmd+,"),
    nib.MenuItem("Check for Updates", action=check_updates, icon="arrow.clockwise"),
    nib.MenuDivider(),
    nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
]

def open_settings():
    print("Opening settings")

def check_updates():
    print("Checking for updates")
```

## Callback Signatures Summary

| View / Feature | Parameter | Callback Signature |
|---|---|---|
| `Button` | `action=` | `def handler():` |
| `TextField` | `on_change=` | `def handler(value: str):` |
| `TextField` | `on_submit=` | `def handler(value: str):` |
| `SecureField` | `on_change=` | `def handler(value: str):` |
| `SecureField` | `on_submit=` | `def handler(value: str):` |
| `TextEditor` | `on_change=` | `def handler(text: str):` |
| `Toggle` | `on_change=` | `def handler(is_on: bool):` |
| `Slider` | `on_change=` | `def handler(value: float):` |
| `Picker` | `on_change=` | `def handler(value: str):` |
| `App` | `on_appear=` | `def handler():` |
| `App` | `on_disappear=` | `def handler():` |
| `App` | `on_quit=` | `def handler():` |
| Any view | `on_drop=` | `def handler(paths: list[str]):` |
| Any view | `on_hover=` | `def handler(is_hovering: bool):` |
| Any view | `on_click=` | `def handler():` |
| `Canvas` | `on_pan_start=` | `def handler(e: PanEvent):` |
| `Canvas` | `on_pan_update=` | `def handler(e: PanEvent):` |
| `Canvas` | `on_pan_end=` | `def handler(e: PanEvent):` |
| `Canvas` | `on_hover=` | `def handler(e: PanEvent):` |
| `MenuItem` | `action=` | `def handler():` |
| `App.on_hotkey` | callback | `def handler():` |

## Event Threading

All event callbacks run on a single dedicated event thread. This means:

- Callbacks never run concurrently with each other.
- You can safely mutate view properties in callbacks without locks.
- Long-running callbacks block subsequent events from being processed.

!!! tip "Avoid blocking the event thread"
    If a callback needs to do heavy work (network requests, file I/O, computation), run it in a separate thread and update the UI from there. View property mutations are thread-safe and will trigger re-renders from any thread.

```python
import threading

def fetch_data():
    status.content = "Loading..."

    def do_fetch():
        import time
        time.sleep(2)  # Simulate network request
        status.content = "Done!"

    threading.Thread(target=do_fetch, daemon=True).start()
```
