# State & Binding

Reactive state primitives for class-based Nib applications. `State` is a Python descriptor that automatically triggers UI re-renders when its value changes. `Binding` wraps getter/setter functions for two-way data flow between state and UI controls.

For function-based apps, you typically mutate view properties directly (e.g. `text.content = "new"`) instead of using `State`.

---

## State

A descriptor that stores per-instance state and calls the owner's `_trigger_rerender()` method whenever the value changes.

### Constructor

```python
nib.State(initial: T)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `initial` | `T` | -- | The initial/default value for this state variable. Can be any type: `int`, `str`, `bool`, `list`, `dict`, etc. |

### Behavior

- Declare as a **class variable** on an `App` subclass.
- Read and write using normal attribute access on the instance (`self.count`).
- When the value changes (compared with `!=`), a re-render is triggered automatically.
- The underlying value is stored in a mangled attribute (`_state_<name>`) to avoid conflicts.
- Accessing the descriptor from the class (not an instance) returns the `State` object itself.

---

## Binding

A two-way binding that wraps a getter and setter function. Useful for controls that need to both read a value and write changes back to state.

### Constructor

```python
nib.Binding(getter: Callable[[], T], setter: Callable[[T], None])
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `getter` | `Callable[[], T]` | -- | A function that returns the current value |
| `setter` | `Callable[[T], None]` | -- | A function that updates the value |

### Properties

| Property | Type | Description |
|---|---|---|
| `value` | `T` | Read/write access to the bound value. Getting calls the getter; setting calls the setter |

---

## Examples

### Basic counter with State

```python
import nib

class CounterApp(nib.App):
    count = nib.State(0)

    def body(self):
        return nib.VStack(
            controls=[
                nib.Text(f"Count: {self.count}", font=nib.Font.TITLE),
                nib.HStack(
                    controls=[
                        nib.Button("- 1", action=self.decrement),
                        nib.Button("+ 1", action=self.increment),
                    ],
                    spacing=8,
                ),
            ],
            spacing=12,
            padding=20,
        )

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

CounterApp(title="Counter", icon="number.circle").run()
```

### Multiple state variables

```python
import nib

class ProfileApp(nib.App):
    name = nib.State("")
    dark_mode = nib.State(False)
    font_size = nib.State(14)

    def body(self):
        return nib.VStack(
            controls=[
                nib.Text(f"Hello, {self.name or 'stranger'}!", font=nib.Font.TITLE),
                nib.TextField(
                    value=self.name,
                    placeholder="Your name",
                    on_change=lambda v: setattr(self, "name", v),
                ),
                nib.Toggle(
                    "Dark Mode",
                    is_on=self.dark_mode,
                    on_change=lambda v: setattr(self, "dark_mode", v),
                ),
                nib.Slider(
                    "Font Size",
                    value=self.font_size,
                    min_value=10,
                    max_value=24,
                    on_change=lambda v: setattr(self, "font_size", v),
                ),
            ],
            spacing=10,
            padding=16,
        )

ProfileApp(title="Profile", icon="person.circle").run()
```

### Using Binding for two-way data flow

```python
import nib
from nib import Binding

class SearchApp(nib.App):
    query = nib.State("")

    def body(self):
        binding = Binding(
            getter=lambda: self.query,
            setter=lambda v: setattr(self, "query", v),
        )

        results = [item for item in ["Apple", "Banana", "Cherry"]
                    if self.query.lower() in item.lower()] if self.query else []

        return nib.VStack(
            controls=[
                nib.TextField(
                    value=binding.value,
                    placeholder="Search fruits...",
                    on_change=binding.value.__class__.__set__,
                ),
                *[nib.Text(r) for r in results],
            ],
            spacing=8,
            padding=16,
        )

SearchApp(title="Search", icon="magnifyingglass").run()
```

## Related

- [App](app.md) -- The base class that `State` descriptors are used with
- [Settings](settings.md) -- Persistent settings (survives app restarts, unlike `State`)
