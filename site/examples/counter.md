# Counter App

A minimal counter application that demonstrates the fundamentals of Nib: app configuration, reactive views, callbacks, context menus, and building the view tree.

## Full Source

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("number")
    app.width = 250
    app.height = 150

    count = nib.Text("0", font=nib.Font.system(48, nib.FontWeight.BOLD))

    def increment():
        count.content = str(int(count.content) + 1)

    def decrement():
        val = int(count.content) - 1
        count.content = str(max(0, val))

    def reset():
        count.content = "0"

    app.menu = [
        nib.MenuItem("Reset", action=reset, icon="arrow.counterclockwise"),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
    ]

    app.build(
        nib.VStack(
            controls=[
                count,
                nib.HStack(
                    controls=[
                        nib.Button("-", action=decrement, style=nib.ButtonStyle.BORDERED),
                        nib.Button("+", action=increment, style=nib.ButtonStyle.BORDERED_PROMINENT),
                    ],
                    spacing=12,
                ),
            ],
            spacing=16,
            padding=24,
        )
    )

nib.run(main)
```

## Walkthrough

### Imports and entry point

```python
import nib
```

The single `import nib` gives you access to every view, layout, type, and utility in the SDK. The `nib.run(main)` call at the bottom starts the app by passing your `main` function to the runtime.

### App configuration

```python
app.title = "Counter"
app.icon = nib.SFSymbol("number")
app.width = 250
app.height = 150
```

These properties control the menu bar appearance and the popover window size:

- `title` sets the text shown next to the icon in the menu bar.
- `icon` accepts an SF Symbol name. Apple provides thousands of built-in icons at [developer.apple.com/sf-symbols](https://developer.apple.com/sf-symbols/).
- `width` and `height` set the popover dimensions in points.

### Creating views

```python
count = nib.Text("0", font=nib.Font.system(48, nib.FontWeight.BOLD))
```

Views are created as Python objects. Here, `nib.Text` displays a string. The `font` parameter uses `nib.Font.system()` to create a system font at size 48 with bold weight.

By storing the view in a variable (`count`), you can modify its properties later to trigger UI updates.

### Defining callbacks

```python
def increment():
    count.content = str(int(count.content) + 1)

def decrement():
    val = int(count.content) - 1
    count.content = str(max(0, val))

def reset():
    count.content = "0"
```

Callbacks are plain Python functions. When a callback assigns a new value to a view property (like `count.content`), Nib's reactivity system automatically diffs the view tree and sends a patch to the Swift runtime. The UI updates immediately.

Note how `decrement` clamps the value at zero using `max(0, val)`.

### Context menu

```python
app.menu = [
    nib.MenuItem("Reset", action=reset, icon="arrow.counterclockwise"),
    nib.MenuDivider(),
    nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
]
```

The `app.menu` property defines the right-click context menu on the status bar icon. Each `MenuItem` takes a label, an optional callback, an optional SF Symbol icon, and an optional keyboard shortcut. `MenuDivider` adds a visual separator.

### Building the view tree

```python
app.build(
    nib.VStack(
        controls=[
            count,
            nib.HStack(
                controls=[
                    nib.Button("-", action=decrement, style=nib.ButtonStyle.BORDERED),
                    nib.Button("+", action=increment, style=nib.ButtonStyle.BORDERED_PROMINENT),
                ],
                spacing=12,
            ),
        ],
        spacing=16,
        padding=24,
    )
)
```

`app.build()` sets the root view. The tree is composed of nested layout containers:

- `VStack` arranges children vertically. The `controls` list contains the count text and a nested `HStack`.
- `HStack` arranges the two buttons horizontally.
- `spacing` sets the gap between children in points.
- `padding` adds space around the entire stack.
- `ButtonStyle.BORDERED` gives a subtle outline; `ButtonStyle.BORDERED_PROMINENT` gives a filled, accented appearance.

### Running the app

```python
nib.run(main)
```

This is the entry point. It creates an `App` instance, passes it to your `main` function, and starts the event loop. The app appears in the menu bar and opens a popover when clicked.

```bash
nib run counter.py
```
