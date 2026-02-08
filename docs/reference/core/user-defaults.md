# UserDefaults

Low-level persistent key-value storage using macOS UserDefaults. Values survive app restarts and are scoped to the application's bundle identifier.

For most use cases, the higher-level [Settings](settings.md) class is preferred. Use `UserDefaults` directly when you need fine-grained control over individual keys or when working outside the settings pattern.

## Constructor

```python
nib.UserDefaults(app=None)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app` | `App \| None` | `None` | The App instance to use for communication with the Swift runtime. If `None`, uses the current running app set by `nib.run()` |

## Supported Value Types

| Python Type | Description |
|---|---|
| `str` | Strings |
| `int` | Integers |
| `float` | Floating point numbers |
| `bool` | Booleans |
| `list` | Lists (must be JSON-serializable) |
| `dict` | Dictionaries (must be JSON-serializable) |
| `bytes` | Binary data (base64-encoded for transport) |

## Methods

### `set(key, value)`

Store a value under the given key.

```python
defaults.set(key: str, value: Any) -> None
```

| Parameter | Type | Description |
|---|---|---|
| `key` | `str` | The key to store the value under |
| `value` | `Any` | The value to store. Must be one of the supported types |

### `get(key, default, timeout)`

Retrieve a value by key. This is a **blocking** call that waits for a response from the Swift runtime.

```python
defaults.get(key: str, default: Any = None, timeout: float = 5.0) -> Any
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `key` | `str` | -- | The key to retrieve |
| `default` | `Any` | `None` | Value returned if the key is not found |
| `timeout` | `float` | `5.0` | Maximum wait time in seconds |

**Returns:** The stored value with its original Python type, or `default` if the key does not exist or the request times out.

### `remove(key)`

Delete a key and its value.

```python
defaults.remove(key: str) -> None
```

| Parameter | Type | Description |
|---|---|---|
| `key` | `str` | The key to remove |

### `clear()`

Remove all keys and values stored by this application.

```python
defaults.clear() -> None
```

### `contains_key(key, timeout)`

Check whether a key exists. This is a **blocking** call.

```python
defaults.contains_key(key: str, timeout: float = 5.0) -> bool
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `key` | `str` | -- | The key to check |
| `timeout` | `float` | `5.0` | Maximum wait time in seconds |

**Returns:** `True` if the key exists, `False` otherwise.

### `get_keys(prefix, timeout)`

Get all stored keys, optionally filtered by a prefix. This is a **blocking** call.

```python
defaults.get_keys(prefix: str = "", timeout: float = 5.0) -> list[str]
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `prefix` | `str` | `""` | Filter keys that start with this string. Pass `""` for all keys |
| `timeout` | `float` | `5.0` | Maximum wait time in seconds |

**Returns:** List of matching key strings.

## Examples

### Storing and retrieving values

```python
import nib

def main(app: nib.App):
    app.title = "Storage"
    app.icon = nib.SFSymbol("externaldrive")
    app.width = 300
    app.height = 200

    defaults = nib.UserDefaults()

    # Store different value types
    defaults.set("username", "alice")
    defaults.set("login_count", 42)
    defaults.set("dark_mode", True)
    defaults.set("favorites", ["python", "swift"])

    # Retrieve values (blocking)
    username = defaults.get("username", default="guest")
    count = defaults.get("login_count", default=0)

    app.build(
        nib.VStack(
            controls=[
                nib.Text(f"User: {username}"),
                nib.Text(f"Logins: {count}"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Checking keys and listing stored data

```python
import nib

def main(app: nib.App):
    app.title = "Keys"
    app.icon = nib.SFSymbol("key")
    app.width = 300
    app.height = 250

    defaults = nib.UserDefaults()

    # Store some prefixed keys
    defaults.set("user.name", "alice")
    defaults.set("user.email", "alice@example.com")
    defaults.set("app.theme", "dark")

    # Check if a key exists
    has_name = defaults.contains_key("user.name")

    # Get all keys with a prefix
    user_keys = defaults.get_keys("user.")

    app.build(
        nib.VStack(
            controls=[
                nib.Text(f"Has user.name: {has_name}"),
                nib.Text(f"User keys: {', '.join(user_keys)}"),
            ],
            spacing=8,
            padding=16,
        )
    )

nib.run(main)
```

### Tracking launch count

```python
import nib

def main(app: nib.App):
    app.title = "Launch Counter"
    app.icon = nib.SFSymbol("arrow.clockwise")
    app.width = 300
    app.height = 120

    defaults = nib.UserDefaults()

    # Increment and persist launch count
    count = defaults.get("launch_count", default=0)
    count += 1
    defaults.set("launch_count", count)

    def reset():
        defaults.remove("launch_count")
        label.content = "Launch count reset. Restart to see 1."

    label = nib.Text(f"This app has been launched {count} time(s).")

    app.build(
        nib.VStack(
            controls=[
                label,
                nib.Button("Reset Counter", action=reset),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

## Related

- [Settings](settings.md) -- Higher-level settings API with caching built on top of UserDefaults
- [App](app.md) -- The `identifier` property controls the UserDefaults storage scope
