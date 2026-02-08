# Architecture

Nib is a two-process system. Python owns the logic. Swift owns the screen. They talk over a Unix socket using MessagePack.

## The Two-Process Model

Every Nib application runs as two cooperating processes:

**Python process** -- your code. It owns the app logic, the view tree, state management, and event handling. When something changes, Python computes the new UI and sends it across the socket.

**Swift process** -- the runtime. It owns native macOS rendering via SwiftUI, system APIs (notifications, clipboard, file dialogs, keychain), and the menu bar icon. It receives view descriptions from Python, renders them natively, and sends user interactions back.

Neither process directly accesses the other's memory. All communication happens through serialized messages over a Unix domain socket.

![Architecture diagram showing Python and Swift communicating over a Unix socket](../assets/img/architecture.svg)

## Communication Protocol

Messages are sent as length-prefixed MessagePack payloads. Each message has a 4-byte big-endian length header followed by the packed data.

```
[4 bytes: length][MessagePack payload]
```

Python and Swift exchange three categories of messages:

### render -- Full View Tree

Sent from Python to Swift. Contains the complete view tree as a flat node list, along with app configuration (icon, title, window size, menu items, hotkeys, fonts).

This is sent on every update. Python re-serializes the entire view tree and sends it to Swift, which replaces the current UI.

```python
# Internal structure (you don't build this manually)
{
    "type": "flatRender",
    "payload": {
        "nodes": [...],          # Flat list of view nodes
        "rootId": "0",           # ID of the root node
        "statusBar": {
            "icon": "star.fill",
            "title": "My App"
        },
        "window": {
            "width": 300.0,
            "height": 400.0
        },
        "menu": [...],           # Right-click menu items
        "hotkeys": ["cmd+k"],    # Global keyboard shortcuts
        "fonts": {...}           # Custom font paths
    }
}
```

### patch -- Incremental Updates

Defined in the protocol but currently unused. Nib sends full renders on every update instead of computing incremental patches. The diff engine exists (`diff.py`) but full renders proved more reliable for the Swift-side view reconciliation.

### event -- User Interactions

Sent from Swift to Python. Carries a node ID and an event string describing what happened.

```python
# Internal structure
{
    "type": "event",
    "nodeId": "0.1.0",        # Which view triggered the event
    "event": "tap"            # What happened
}
```

Event string formats:

| Event | Format | Example |
|---|---|---|
| Button tap | `tap` | `tap` |
| Value change | `change:<value>` | `change:hello` |
| Submit | `submit:<value>` | `submit:search query` |
| Drop files | `drop:<paths>` | `drop:/path/to/file.txt` |
| Hover | `hover:<bool>` | `hover:true` |
| Click | `click` | `click` |
| Canvas pan | `pan:<type>:<x>,<y>` | `pan:update:150.0,200.0` |
| Hotkey | `hotkey:<shortcut>` | `hotkey:cmd+shift+n` |
| Lifecycle | `appear` / `disappear` | `appear` |

## Execution Modes

### Development Mode (`nib run`)

Python is the parent process. It launches the Swift runtime as a subprocess, passing the socket path via environment variable.

```
Python (parent)
  |
  +-- Spawns Swift runtime subprocess
  |
  +-- Creates Unix socket at /tmp/nib-<pid>.sock
  |
  +-- Connects and starts message loop
```

In this mode, `nib run` also watches your Python files for changes and restarts the app automatically (hot reload).

### Bundled Mode (standalone `.app`)

Swift is the parent process. The `.app` bundle contains both the Swift runtime and your Python code. When launched, Swift starts and spawns Python as a child process.

```
Swift Runtime (parent, inside .app bundle)
  |
  +-- Creates Unix socket
  |
  +-- Spawns Python with NIB_SOCKET env var
  |
  +-- Python connects to the provided socket
```

The `NIB_SOCKET` environment variable tells Python it is running in bundled mode and where to find the socket.

!!! info "Same protocol, different launcher"
    The message protocol is identical in both modes. The only difference is which process starts first and who creates the socket. Your Python code does not need to change between development and production.

## Data Flow: From Property Change to Pixel

Here is the complete path when you mutate a view property:

```
1. Python: text.content = "new value"
       |
2. View.__setattr__ detects change, calls app._trigger_rerender()
       |
3. App sets _render_requested event (threading.Event)
       |
4. Render loop thread wakes up, calls _render()
       |
5. App calls body() to get the root view
       |
6. App calls _collect_actions() to assign IDs and register callbacks
       |
7. Root view serialized to flat node list via to_flat_list()
       |
8. Connection.send_flat_render() packs with MessagePack, sends over socket
       |
9. Swift SocketServer reads length-prefixed message, unpacks
       |
10. Swift AppDelegate routes to ViewStore
       |
11. SwiftUI observes ViewStore change, re-renders affected views
       |
12. Native macOS pixels update on screen
```

!!! note "Coalesced rendering"
    Multiple rapid property changes are coalesced into a single render. The render loop uses a threading Event that is set on any change and cleared when a render begins. This means if you change three properties in quick succession, only one render happens. The render loop is throttled to approximately 500 frames per second maximum.

## Other Message Types

Beyond the core three, Python sends additional message types for system integration:

| Message Type | Direction | Purpose |
|---|---|---|
| `quit` | Python to Swift | Terminate the runtime |
| `notify` | Python to Swift | Show a macOS notification |
| `clipboard` | Python to Swift | Read/write the system clipboard |
| `fileDialog` | Python to Swift | Open/save file picker dialogs |
| `userDefaults` | Python to Swift | Persist settings via UserDefaults |
| `service` | Python to Swift | Query system services (battery, screen, etc.) |
| `action` | Python to Swift | Trigger view-specific actions (WebView reload, etc.) |
| `settingsRender` | Python to Swift | Send settings window UI |
| `notification` | Python to Swift | Push/schedule/cancel notifications |
| `serviceResponse` | Swift to Python | System service query results |
| `notificationResponse` | Swift to Python | Notification action responses |
| `fileDialogResponse` | Swift to Python | File dialog selections |
