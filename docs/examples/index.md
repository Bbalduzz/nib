# Examples

Complete, runnable example applications that demonstrate how to build real menu bar apps with Nib. Each example includes full source code with a step-by-step explanation.

## Gallery

| Example | Description |
|---------|-------------|
| [Counter App](counter.md) | A minimal counter with increment, decrement, and reset. Covers app configuration, reactive text, callbacks, context menus, and the view tree |
| [Todo App](todo.md) | A task list with add, complete, and delete. Demonstrates TextField input, List and Section layout, Toggle for completion, and dynamic view updates |
| [System Monitor](system-monitor.md) | A dashboard showing battery, network, display, and thermal info. Uses multiple system services, `on_appear` for auto-refresh, and card-style layouts |
| [Drawing App](drawing-app.md) | A freehand drawing canvas with color and width selectors. Demonstrates the Canvas view, pan gesture handling, and the `nib.draw` module |

## Running Examples

All examples follow the same pattern. Save the code to a `.py` file and run it with:

```bash
nib run your_example.py
```

Or, for development with hot reload on file changes:

```bash
nib run your_example.py -r
```

## Template

Every Nib app follows this structure:

```python
import nib

def main(app: nib.App):
    # 1. Configure the app
    app.title = "My App"
    app.icon = nib.SFSymbol("star")
    app.width = 300
    app.height = 200

    # 2. Create views
    label = nib.Text("Hello")

    # 3. Define callbacks
    def on_click():
        label.content = "Clicked!"

    # 4. Build the view tree
    app.build(
        nib.VStack(
            controls=[label, nib.Button("Click", action=on_click)],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```
