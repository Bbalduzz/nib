# App

The main application class for Nib menu bar applications. `App` manages the entire lifecycle of a Nib application, including window configuration, view rendering, event handling, system integration, and communication with the Swift runtime.

## Constructor

```python
nib.App(title=None, icon=None, identifier=None)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str \| None` | `None` | Text displayed in the menu bar next to the icon |
| `icon` | `str \| SFSymbol \| None` | `None` | Menu bar icon. Pass an SF Symbol name string or an `SFSymbol` instance |
| `identifier` | `str \| None` | `None` | Bundle identifier used for UserDefaults storage. Defaults to `"com.nib.<title>"` |

## Properties

### Window and Appearance

| Property | Type | Description |
|---|---|---|
| `title` | `str` | Text displayed in the menu bar. Readable and writable |
| `icon` | `str \| SFSymbol \| View` | Menu bar icon. Accepts an SF Symbol name, `SFSymbol` instance, or any `View` |
| `identifier` | `str` | Bundle identifier. If not set, derives from title as `"com.nib.<normalized_title>"` |
| `width` | `float` | Popover window width in points |
| `height` | `float` | Popover window height in points |
| `show_quit_item` | `bool` | When `True`, appends a styled "Quit" button at the bottom of the app UI |

### Menu and Fonts

| Property | Type | Description |
|---|---|---|
| `menu` | `list[MenuItem]` | Right-click context menu items for the status bar icon |
| `fonts` | `dict[str, str]` | Custom fonts registered for the app. Maps font names to file paths or URLs. Fonts placed in `assets/fonts/` are auto-detected |

### Lifecycle Callbacks

| Property | Type | Description |
|---|---|---|
| `on_appear` | `Callable[[], None]` | Called every time the popover opens |
| `on_disappear` | `Callable[[], None]` | Called every time the popover closes |
| `on_quit` | `Callable[[], None]` | Called once when the app shuts down, before cleanup |

### Settings

| Property | Type | Description |
|---|---|---|
| `settings` | `SettingsPage` | Settings page configuration. When set, the preferences window is accessible via Cmd+, |
| `clipboard` | `str` | Write-only setter for clipboard content. Use `get_clipboard()` for reading |

### Service Properties (read-only)

| Property | Type | Description |
|---|---|---|
| `notifications` | `NotificationManager` | Push, schedule, and manage macOS notifications |
| `battery` | `Battery` | Read battery level and charging state |
| `connectivity` | `Connectivity` | Check network connectivity status |
| `screen` | `Screen` | Get display info and control brightness |
| `keychain` | `Keychain` | Secure storage for passwords and tokens |
| `camera` | `Camera` | List devices, capture photos, access video frames |
| `launch_at_login` | `LaunchAtLogin` | Control whether the app starts on login |
| `permissions` | `Permissions` | Check and request Camera, Microphone, and Notification permissions |

## Methods

### View Management

#### `build(view)`

Set the root view of the application. If the app is already running, triggers an immediate re-render.

```python
app.build(view: View) -> None
```

| Parameter | Type | Description |
|---|---|---|
| `view` | `View` | The root view to display in the popover |

#### `body()`

Override this method in a subclass to define the UI. Returns the root view. Only used in the class-based approach.

```python
app.body() -> View
```

#### `update()`

Manually trigger a UI re-render. Use this to force an update when the automatic reactivity system might not detect a change, or to batch multiple changes into a single render pass.

```python
app.update() -> None
```

### Application Lifecycle

#### `run()`

Start the application. Connects to the Swift runtime, performs the initial render, and enters the main event loop. Blocks until the app quits.

```python
app.run() -> None
```

#### `quit()`

Quit the application and clean up resources.

```python
app.quit() -> None
```

### Notifications

#### `notify(title, body, subtitle, sound, identifier)`

Send a macOS system notification.

```python
app.notify(
    title: str,
    body: str | None = None,
    subtitle: str | None = None,
    sound: bool = True,
    identifier: str | None = None,
) -> None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `str` | -- | Notification title (required) |
| `body` | `str \| None` | `None` | Notification body text |
| `subtitle` | `str \| None` | `None` | Subtitle shown below the title |
| `sound` | `bool` | `True` | Play the default notification sound |
| `identifier` | `str \| None` | `None` | Unique ID for updating or removing the notification later |

### Clipboard

#### `get_clipboard(callback)`

Read clipboard content asynchronously. The callback receives the clipboard string.

```python
app.get_clipboard(callback: Callable[[str], None]) -> None
```

#### `set_clipboard(content)`

Set clipboard content. Equivalent to `app.clipboard = content`.

```python
app.set_clipboard(content: str) -> None
```

### Hotkeys

#### `on_hotkey(shortcut, callback)`

Register a global keyboard shortcut.

```python
app.on_hotkey(shortcut: str, callback: Callable[[], None]) -> None
```

| Parameter | Type | Description |
|---|---|---|
| `shortcut` | `str` | Key combination, e.g. `"cmd+shift+n"`, `"cmd+k"` |
| `callback` | `Callable` | Function called when the hotkey is pressed |

#### `hotkey(shortcut)`

Decorator form of `on_hotkey`.

```python
@app.hotkey("cmd+shift+n")
def show_window():
    pass
```

### Settings

#### `register_settings(settings)`

Register a `Settings` object for persistence. Connects the settings to UserDefaults and waits for initial values to load.

```python
app.register_settings(settings: Settings) -> None
```

#### `open_settings()`

Open the settings window programmatically.

```python
app.open_settings() -> None
```

#### `close_settings()`

Close the settings window programmatically.

```python
app.close_settings() -> None
```

### Class Methods

#### `set_assets_dir(path)`

Set the assets directory for the application. Relative paths are resolved from the main script directory.

```python
App.set_assets_dir(path: str | Path | None) -> None
```

#### `resolve_asset(relative_path)`

Resolve a relative asset path to an absolute path. Returns the input unchanged for absolute paths and URLs. Returns an empty string if the asset is not found.

```python
App.resolve_asset(relative_path: str) -> str
```

## Examples

### Function-based app (recommended)

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("number.circle")
    app.width = 280
    app.height = 150

    label = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        label.content = str(int(label.content) + 1)

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Button("Increment", action=increment),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Class-based app

```python
import nib

class CounterApp(nib.App):
    count = nib.State(0)

    def body(self):
        return nib.VStack(
            controls=[
                nib.Text(f"Count: {self.count}", font=nib.Font.TITLE),
                nib.Button("Increment", action=self.increment),
            ],
            spacing=12,
            padding=20,
        )

    def increment(self):
        self.count += 1

CounterApp(title="Counter", icon="number.circle").run()
```

### Full-featured app with menu, hotkeys, and settings

```python
import nib

def main(app: nib.App):
    app.title = "Notes"
    app.icon = nib.SFSymbol("note.text")
    app.width = 400
    app.height = 300

    settings = nib.Settings({"dark_mode": False, "font_size": 14})
    app.register_settings(settings)

    editor = nib.TextEditor(text="", placeholder="Start typing...")

    app.menu = [
        nib.MenuItem("Preferences", action=app.open_settings, icon="gear", shortcut="cmd+,"),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
    ]

    @app.hotkey("cmd+shift+n")
    def new_note():
        editor.text = ""

    app.on_appear = lambda: print("Popover opened")

    app.build(
        nib.VStack(
            controls=[editor],
            padding=16,
        )
    )

nib.run(main)
```

## Related

- [run()](run.md) -- Recommended entry point for function-based apps
- [SFSymbol](sfsymbol.md) -- Menu bar icons
- [MenuItem & MenuDivider](menu.md) -- Context menu items
- [Settings](settings.md) -- Persistent settings
- [SettingsPage](settings-page.md) -- Preferences window
