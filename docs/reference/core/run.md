# run()

The recommended entry point for Nib applications. Creates an `App` instance, passes it to your main function for configuration, then starts the application event loop.

## Signature

```python
nib.run(main: Callable[[App], None], assets_dir: str | Path | None = None) -> None
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `main` | `Callable[[App], None]` | -- | A function that receives an `App` instance and configures it by setting properties and calling `app.build()` |
| `assets_dir` | `str \| Path \| None` | `None` | Path to the assets directory. When `None`, Nib auto-detects an `assets/` folder relative to the script. Relative paths resolve from the main script directory |

## Behavior

1. If `assets_dir` is provided, calls `App.set_assets_dir(assets_dir)`.
2. Creates a new `App()` instance.
3. Registers it as the current app (for `UserDefaults` and `FilePicker` to use by default).
4. Calls `main(app)` so you can configure the app.
5. Calls `app.run()` to connect to the Swift runtime and enter the event loop.
6. Cleans up when the app exits.

## Examples

### Basic usage

```python
import nib

def main(app: nib.App):
    app.title = "Hello"
    app.icon = nib.SFSymbol("hand.wave")
    app.width = 300
    app.height = 200

    app.build(
        nib.Text("Hello, World!", font=nib.Font.TITLE, padding=20)
    )

nib.run(main)
```

### With custom assets directory

```python
import nib

def main(app: nib.App):
    app.title = "Gallery"
    app.icon = nib.SFSymbol("photo")
    app.width = 400
    app.height = 300

    # "logo.png" resolves to "my_assets/logo.png"
    app.build(
        nib.Image(source="logo.png", width=200, height=200)
    )

nib.run(main, assets_dir="my_assets")
```

### Interactive counter

```python
import nib

def main(app: nib.App):
    app.title = "Counter"
    app.icon = nib.SFSymbol("plus.circle")
    app.width = 250
    app.height = 120

    counter = nib.Text("0", font=nib.Font.LARGE_TITLE)

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

## Related

- [App](app.md) -- The application class configured inside the `main` function
- [SFSymbol](sfsymbol.md) -- Icons used for `app.icon`
