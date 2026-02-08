# Reactivity

Nib uses a simple reactivity model: mutate a view property, and the UI updates automatically. There is no virtual DOM, no signals, no subscription system. You change a value; Nib detects it and sends the new view tree to Swift.

## How It Works

Every view holds a reference to the parent `App`. When you set a property on a view (e.g., `text.content = "new value"`), the `View.__setattr__` override detects the change and calls `app._trigger_rerender()`. This sets a threading Event that wakes the render loop, which re-serializes the entire view tree and sends it to Swift.

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("number")
    app.width = 300
    app.height = 200

    counter = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        counter.content = str(int(counter.content) + 1)  # Triggers re-render

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

When the button is tapped, `increment()` runs, setting `counter.content`. This triggers a full re-render: the view tree is re-serialized and sent to Swift, which updates the native UI.

## The Render Loop

The render loop runs on a dedicated background thread. It is event-based and coalesced:

1. A property change calls `app._trigger_rerender()`, which sets a `threading.Event`.
2. The render thread is waiting on this event. When set, it wakes up.
3. The event is cleared, and a render happens.
4. The thread sleeps for 2ms (minimum interval), then waits again.

This design means rapid consecutive changes are coalesced into a single render:

```python
# These three changes result in ONE render, not three
label1.content = "Updated"
label2.content = "Also updated"
label3.opacity = 0.5
```

The maximum render rate is approximately 500 fps. In practice, renders happen much less frequently since they are driven by user events.

## Manual Updates

Sometimes you modify data that the reactivity system cannot detect -- for example, mutating a list in place or changing a nested object. In those cases, call `app.update()` to force a re-render:

```python
items = ["Apple", "Banana"]
item_list = nib.VStack(
    controls=[nib.Text(item) for item in items],
    spacing=4,
)

def add_item():
    items.append("Cherry")
    # Rebuild the controls list
    item_list._children = [nib.Text(item) for item in items]
    for child in item_list._children:
        child._set_app(app)
    app.update()  # Force re-render
```

!!! tip "When to use app.update()"
    You rarely need `app.update()`. Direct property mutations on views (like `text.content = "new"` or `view.opacity = 0.5`) automatically trigger re-renders. Use `app.update()` only when you are modifying data structures that views reference indirectly.

## Function-Based Reactivity

The recommended approach. You create view instances, keep references to them, and mutate their properties directly:

```python
import nib

def main(app: nib.App):
    status = nib.Text("Idle", foreground_color=nib.Color.SECONDARY_LABEL)
    progress = nib.ProgressView(value=0.0)
    start_button = nib.Button("Start", action=None)

    def start_task():
        status.content = "Running..."
        status.foreground_color = nib.Color.BLUE
        start_button.visible = False
        # Simulate progress updates
        for i in range(10):
            import time
            time.sleep(0.1)
            progress.value = (i + 1) / 10

        status.content = "Done"
        status.foreground_color = nib.Color.GREEN
        start_button.visible = True

    start_button._action = start_task

    app.build(
        nib.VStack(
            controls=[status, progress, start_button],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

Every property assignment (`status.content = ...`, `progress.value = ...`, `start_button.visible = ...`) triggers a re-render automatically.

## Class-Based Reactivity

For class-based apps, Nib provides the `State[T]` descriptor. When you assign to a `State` attribute, it calls `_trigger_rerender()` on the app instance:

```python
import nib

class CounterApp(nib.App):
    count = nib.State(0)

    def body(self) -> nib.View:
        return nib.VStack(
            controls=[
                nib.Text(f"Count: {self.count}", font=nib.Font.TITLE),
                nib.Button("Increment", action=self.increment),
            ],
            spacing=8,
            padding=16,
        )

    def increment(self):
        self.count += 1  # State descriptor triggers re-render

CounterApp(icon="number").run()
```

!!! note "Class-based rebuilds the tree"
    In the class-based approach, `body()` is called on every render, creating new view instances each time. In the function-based approach, you mutate existing instances. Both work; the function-based approach is recommended because it avoids object allocation overhead.

## Reactive Modifiers

View modifiers (styling properties) are also reactive. Changing a modifier triggers a re-render just like changing content:

```python
box = nib.VStack(
    controls=[nib.Text("Hello")],
    background="#333333",
    opacity=1.0,
    padding=16,
)

def fade_out():
    box.opacity = 0.3           # Triggers re-render
    box.background = "#ff0000"  # Triggers re-render
```

The following modifier properties can be mutated reactively on any view:

- `width`, `height`, `min_width`, `min_height`, `max_width`, `max_height`
- `padding`, `margin`
- `background`, `foreground_color`, `fill`, `stroke`, `stroke_width`
- `opacity`, `corner_radius`
- `font`, `font_weight`
- `shadow_color`, `shadow_radius`, `shadow_x`, `shadow_y`
- `border_color`, `border_width`
- `clip_shape`, `blend_mode`, `scale`, `offset`
- `animation`, `content_transition`, `transition`
- `visible`

## No Virtual DOM

Nib does not use a virtual DOM or a reconciliation algorithm on the Python side. The diff engine (`diff.py`) exists but is currently unused. Instead, on every render, the full view tree is serialized to a flat node list and sent to Swift. Swift's SwiftUI framework handles the actual view diffing and only repaints what changed on screen.

This approach is simple and fast enough because:

- Menu bar apps typically have small view trees (tens to low hundreds of nodes).
- MessagePack serialization is fast.
- SwiftUI is efficient at diffing and partial re-renders.
- The render loop coalesces rapid changes.

## Batching Changes

If you are making several changes and want a single render, you can rely on the natural coalescing behavior -- consecutive property mutations in the same function call will be coalesced by the render loop:

```python
def update_everything():
    title.content = "New Title"
    subtitle.content = "New Subtitle"
    icon.foreground_color = nib.Color.RED
    container.opacity = 0.8
    # All four changes coalesce into one render
```

If you need explicit control, you can batch changes and call `app.update()` once at the end:

```python
def update_everything():
    title.content = "New Title"
    subtitle.content = "New Subtitle"
    icon.foreground_color = nib.Color.RED
    container.opacity = 0.8
    app.update()  # Explicit single render
```
