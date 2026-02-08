# Assets

Nib provides an asset system for managing images, fonts, and other files used by your application. Assets are resolved automatically in both development and bundled modes.

## Assets directory

Place your asset files in an `assets/` directory next to your script:

```
myapp/
├── src/
│   ├── main.py
│   └── assets/
│       ├── logo.png
│       ├── icon.png
│       └── fonts/
│           └── Geist-Regular.ttf
```

Nib auto-detects the assets directory by searching these locations (in order):

1. `<script_dir>/assets` -- same directory as your main script
2. `<script_dir>/../assets` -- parent directory (if your script is in `src/`)
3. `<script_dir>/src/assets` -- `src/assets` from the project root

!!! note
    The `nib create` command scaffolds a project with `src/assets/` already in place.

## Manual configuration

If your assets are in a non-standard location, set the path explicitly:

```python
import nib

nib.App.set_assets_dir("path/to/my/assets")
```

Relative paths are resolved relative to your script's directory. You can also pass an absolute path:

```python
nib.App.set_assets_dir("/Users/me/shared-assets")
```

Or set it when calling `nib.run()`:

```python
nib.run(main, assets_dir="my_assets")
```

## Resolving asset paths

Use `App.resolve_asset()` to convert a relative asset path to an absolute path:

```python
logo_path = nib.App.resolve_asset("images/logo.png")
# Returns: "/Users/me/myapp/src/assets/images/logo.png"
```

The method handles both development and bundled modes transparently.

### Resolution rules

- **Absolute paths** (`/Users/me/file.png`) are returned as-is
- **URLs** (`https://example.com/image.png`) are returned as-is
- **Relative paths** (`images/logo.png`) are resolved relative to the assets directory
- If the asset is not found, an empty string is returned and a warning is logged

## Using assets in views

### Images

The `Image` view resolves paths relative to the assets directory automatically:

```python
# Resolves to assets/logo.png
nib.Image(source="logo.png")

# Subdirectory
nib.Image(source="images/hero.png")

# Absolute path (bypasses assets resolution)
nib.Image(source="/Users/me/Desktop/photo.jpg")

# URL (downloaded by Swift runtime)
nib.Image(source="https://example.com/image.png")
```

### Fonts

Font files placed in the assets directory are auto-detected. See the [Custom Fonts](custom-fonts.md) guide for details.

### Other files

For non-view assets (data files, templates, etc.), use `resolve_asset()` to get the path and then read the file normally:

```python
config_path = nib.App.resolve_asset("config.json")
if config_path:
    import json
    with open(config_path) as f:
        config = json.load(f)
```

## Development vs. bundled mode

The asset system works transparently across both modes:

### Development mode (`nib run`)

In development mode, asset paths point directly to your project's `assets/` directory on disk. Changes to asset files are picked up immediately.

```
Project directory:
  src/assets/logo.png
  -> resolves to /Users/me/myapp/src/assets/logo.png
```

### Bundled mode (`nib build`)

When you build a standalone `.app` bundle with `nib build`, assets are copied into the `Contents/Resources/assets` directory inside the app bundle:

```
MyApp.app/
└── Contents/
    ├── MacOS/
    │   └── ...
    └── Resources/
        ├── app/
        │   └── main.py (or .pyc)
        └── assets/
            ├── logo.png
            └── fonts/
                └── Geist-Regular.ttf
```

Nib detects bundled mode automatically and resolves assets from `Contents/Resources/assets`. No code changes are needed when switching between development and production.

## Organizing assets

A recommended structure for larger projects:

```
assets/
├── images/
│   ├── logo.png
│   ├── icon.png
│   └── backgrounds/
│       └── hero.png
├── fonts/
│   ├── Geist-Regular.ttf
│   └── Geist-Bold.ttf
└── data/
    └── defaults.json
```

Use subdirectory paths when referencing assets:

```python
nib.Image(source="images/logo.png")
nib.Image(source="images/backgrounds/hero.png")

config_path = nib.App.resolve_asset("data/defaults.json")
```

## Complete example

```python
import nib
import json


def main(app: nib.App):
    app.title = "Gallery"
    app.icon = nib.SFSymbol("photo.stack")
    app.width = 350
    app.height = 400

    # Load image names from a JSON manifest in assets
    manifest_path = nib.App.resolve_asset("manifest.json")
    if manifest_path:
        with open(manifest_path) as f:
            image_names = json.load(f)
    else:
        image_names = ["photo1.png", "photo2.png"]

    current_index = 0
    image_view = nib.Image(
        source=f"images/{image_names[current_index]}",
        width=300,
        height=250,
        corner_radius=8,
    )
    counter = nib.Text(
        f"1 / {len(image_names)}",
        foreground_color=nib.Color.GRAY,
    )

    def next_image():
        nonlocal current_index
        current_index = (current_index + 1) % len(image_names)
        image_view.source = f"images/{image_names[current_index]}"
        counter.content = f"{current_index + 1} / {len(image_names)}"

    def prev_image():
        nonlocal current_index
        current_index = (current_index - 1) % len(image_names)
        image_view.source = f"images/{image_names[current_index]}"
        counter.content = f"{current_index + 1} / {len(image_names)}"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Photo Gallery", font=nib.Font.TITLE),
                image_view,
                nib.HStack(
                    controls=[
                        nib.Button("Previous", action=prev_image),
                        nib.Spacer(),
                        counter,
                        nib.Spacer(),
                        nib.Button("Next", action=next_image),
                    ],
                ),
            ],
            spacing=12,
            padding=16,
        )
    )


nib.run(main)
```

!!! tip
    Use `nib.App.resolve_asset()` only when you need the absolute path for Python file operations. For view parameters like `nib.Image(source=...)`, pass the relative path directly -- the Swift runtime resolves it automatically.
