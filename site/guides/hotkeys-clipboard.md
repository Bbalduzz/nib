# Hotkeys & Clipboard

Nib provides global keyboard shortcuts (hotkeys) and clipboard access for integrating your menu bar app with system-wide workflows.

## Global hotkeys

Register a global keyboard shortcut that works even when your app's popover is not visible:

```python
import nib


def main(app: nib.App):
    app.title = "Hotkey Demo"
    app.icon = nib.SFSymbol("keyboard")
    app.width = 300
    app.height = 200

    status = nib.Text("Press Cmd+Shift+N", font=nib.Font.HEADLINE)

    def on_shortcut():
        status.content = "Hotkey pressed!"

    app.on_hotkey("cmd+shift+n", on_shortcut)

    app.build(
        nib.VStack(
            controls=[status],
            padding=24,
        )
    )


nib.run(main)
```

### Modifier keys

Combine modifier keys with `+`:

| Modifier | Key name |
|----------|----------|
| Command | `cmd` |
| Shift | `shift` |
| Control | `ctrl` |
| Option/Alt | `opt` or `alt` |

Examples of valid shortcut strings:

```python
app.on_hotkey("cmd+k", callback)
app.on_hotkey("cmd+shift+n", callback)
app.on_hotkey("ctrl+opt+p", callback)
app.on_hotkey("cmd+shift+ctrl+r", callback)
```

!!! note
    Hotkey strings are case-insensitive. `"cmd+shift+N"` and `"cmd+shift+n"` are equivalent.

### Decorator syntax

Use the `@app.hotkey()` decorator as an alternative to `app.on_hotkey()`:

```python
@app.hotkey("cmd+shift+n")
def create_new():
    print("Creating new item...")

@app.hotkey("cmd+k")
def toggle_search():
    print("Toggle search...")
```

The decorator returns the original function, so you can still call it directly if needed.

### Multiple hotkeys

Register as many hotkeys as you need:

```python
app.on_hotkey("cmd+1", lambda: switch_tab(0))
app.on_hotkey("cmd+2", lambda: switch_tab(1))
app.on_hotkey("cmd+3", lambda: switch_tab(2))
app.on_hotkey("cmd+shift+c", copy_selection)
app.on_hotkey("cmd+shift+v", paste_special)
```

## Clipboard

### Writing to clipboard

Set the clipboard content directly with a string assignment:

```python
app.clipboard = "Hello, World!"
```

Or use the method form:

```python
app.set_clipboard("Hello, World!")
```

Both are equivalent. The content is sent to the system clipboard immediately.

### Reading from clipboard

Clipboard reads are asynchronous because they require a round trip to the Swift runtime. Use `get_clipboard()` with a callback:

```python
def on_clipboard(content: str):
    print(f"Clipboard contains: {content}")

app.get_clipboard(on_clipboard)
```

The callback receives the current clipboard text as a string.

## Complete example

A clipboard manager app with hotkey integration:

```python
import nib


def main(app: nib.App):
    app.title = "Clippy"
    app.icon = nib.SFSymbol("doc.on.clipboard")
    app.width = 320
    app.height = 400

    history = []
    history_list = nib.VStack(controls=[], spacing=4)
    status = nib.Text("Ready", foreground_color=nib.Color.GRAY, font=nib.Font.CAPTION)

    def update_list():
        items = []
        for i, text in enumerate(history[-10:]):
            preview = text[:50] + ("..." if len(text) > 50 else "")

            def make_copy(t=text):
                app.clipboard = t
                status.content = "Copied to clipboard"

            items.append(
                nib.Button(
                    content=nib.HStack(
                        controls=[
                            nib.Text(
                                preview,
                                font=nib.Font.system(12),
                            ),
                            nib.Spacer(),
                        ],
                        spacing=4,
                    ),
                    action=make_copy,
                )
            )
        history_list._children = items
        app.update()

    def capture_clipboard():
        def on_read(content: str):
            if content and (not history or history[-1] != content):
                history.append(content)
                status.content = f"Captured: {len(history)} items"
                update_list()
        app.get_clipboard(on_read)

    def clear_history():
        history.clear()
        history_list._children = []
        status.content = "History cleared"
        app.update()

    # Global hotkey to capture current clipboard
    app.on_hotkey("cmd+shift+c", capture_clipboard)

    app.menu = [
        nib.MenuItem("Capture Clipboard", action=capture_clipboard, shortcut="cmd+shift+c"),
        nib.MenuItem("Clear History", action=clear_history),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.HStack(
                    controls=[
                        nib.Text("Clipboard History", font=nib.Font.HEADLINE),
                        nib.Spacer(),
                        nib.Button("Capture", action=capture_clipboard),
                    ],
                ),
                nib.Divider(),
                nib.ScrollView(
                    controls=[history_list],
                ),
                nib.Divider(),
                status,
            ],
            spacing=8,
            padding=12,
        )
    )


nib.run(main)
```

Press `Cmd+Shift+C` from anywhere to capture the current clipboard content into the history. Click any entry to copy it back to the clipboard.

!!! tip
    Global hotkeys work even when the popover is closed. This makes them useful for system-wide actions like toggling visibility, capturing clipboard contents, or triggering background tasks.
