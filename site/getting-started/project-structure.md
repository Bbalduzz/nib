# Project Structure

This page covers the standard layout of a Nib project, how assets are discovered, and how to configure your app through `pyproject.toml`.

## Standard layout

A project created with `nib create` follows this structure:

```
myapp/
├── src/
│   ├── main.py          # Application entry point
│   └── assets/          # Icons, images, fonts
│       └── .gitkeep
├── pyproject.toml       # Project metadata and Nib build config
└── README.md
```

You are free to organize your Python code however you like -- Nib only needs to know the path to your entry point script. The layout above is a convention, not a requirement.

## Entry point

The entry point is the Python file that contains your `nib.run(main)` or `MyApp().run()` call. It is specified in two places:

- **Development mode** -- passed as an argument to `nib run`:
  ```bash
  nib run src/main.py
  ```
- **Build mode** -- configured in `pyproject.toml`:
  ```toml
  [tool.nib]
  entry = "src/main.py"
  ```

## Assets directory

The `assets/` directory holds images, icons, fonts, and any other static files your app needs. Nib auto-detects the assets directory at startup by looking in these locations (in order):

1. `assets/` next to the entry point script
2. `assets/` in the parent directory (handles `src/main.py` finding `assets/` at root)
3. `src/assets/` from the working directory

For example, with the standard layout, running `nib run src/main.py` will find `src/assets/` automatically.

!!! tip
    You can override the auto-detected path by passing `assets_dir` to `nib.run()`:
    ```python
    nib.run(main, assets_dir="my_custom_assets")
    ```
    Or set it explicitly before running:
    ```python
    nib.App.set_assets_dir("/absolute/path/to/assets")
    ```

### Referencing assets in code

Use relative paths from the assets directory when referencing files. Nib resolves them to absolute paths automatically:

```python
# If assets/logo.png exists:
nib.Image(source="logo.png")

# Subdirectories work too:
nib.Image(source="icons/settings.png")
```

Absolute paths and URLs are passed through without resolution:

```python
nib.Image(source="/Users/me/photos/cat.jpg")
nib.Image(source="https://example.com/image.png")
```

## Fonts

Nib automatically detects font files placed in the assets directory. Supported formats are `.ttf`, `.otf`, `.ttc`, `.woff`, and `.woff2`.

Place your font files anywhere inside `assets/`:

```
src/assets/
├── Geist-Regular.ttf
├── Geist-Bold.ttf
└── icons/
    └── app-icon.png
```

The font name is derived from the filename without the extension. Use it with `Font.custom()`:

```python
nib.Text(
    "Hello, custom font!",
    font=nib.Font.custom("Geist-Regular", size=16),
)
```

You can also register fonts from arbitrary paths or URLs using `app.fonts`:

```python
app.fonts = {
    "MyFont": "/absolute/path/to/MyFont.ttf",
    "WebFont": "https://example.com/fonts/WebFont.otf",
}
```

!!! note
    Fonts placed in the assets directory are registered automatically and do not need to be added to `app.fonts`. User-specified fonts in `app.fonts` take precedence if there is a name conflict.

## Images

Place image files (`.png`, `.jpg`, `.svg`, etc.) in the assets directory and reference them by relative path:

```python
# assets/icon.png
nib.Image(source="icon.png", width=64, height=64)

# assets/photos/banner.jpg
nib.Image(source="photos/banner.jpg", content_mode=nib.ContentMode.FIT)
```

For the app icon used in `nib build`, place an `icon.png` at `src/assets/icon.png`. The build system converts it to `.icns` format automatically.

## pyproject.toml configuration

The `[tool.nib]` section configures the Nib CLI. The `[tool.nib.build]` section controls the `nib build` command.

### Entry point

```toml
[tool.nib]
entry = "src/main.py"
```

This tells `nib build` which file to use as the application entry point.

### Build configuration

```toml
[tool.nib.build]
# App display name (defaults to project name)
name = "My App"

# Bundle identifier (defaults to com.nib.<name>)
identifier = "com.example.myapp"

# App version (defaults to project version)
version = "1.0.0"

# App icon (defaults to src/assets/icon.png if it exists)
icon = "src/assets/icon.png"

# Minimum macOS version (defaults to current)
min_macos = "14.0"

# Packages to exclude from bundling
exclude = []

# Extra dependencies to include if auto-detection misses them
extra_deps = []
```

### Info.plist options

Advanced options for the macOS application bundle:

```toml
[tool.nib.build.plist]
copyright = "Copyright 2025 Your Name"
category = "public.app-category.utilities"
notification_style = "banner"    # "banner", "alert", or "none"
dock_icon = false                # true to show in Dock
url_schemes = ["myapp"]          # Custom URL schemes

# Privacy usage descriptions
[tool.nib.build.plist.usage]
camera = "This app needs camera access for video capture."
microphone = "This app needs microphone access for recording."
```

## Development mode vs bundled mode

Nib apps behave differently depending on how they are launched:

### Development mode (`nib run`)

- Python launches the Swift runtime as a child process.
- Assets are read directly from the filesystem using the auto-detected path.
- File changes trigger hot reload -- the Python process restarts while the Swift runtime stays alive.

### Bundled mode (`nib build` output)

- The Swift runtime is the main executable. It launches an embedded Python interpreter.
- Assets are bundled inside the `.app` at `Contents/Resources/assets/`.
- The `NIB_SOCKET` environment variable is set by the Swift runtime so Python knows it is running in bundled mode.

!!! warning
    Paths that work in development (e.g., `../../data/file.txt`) may not work in a bundled app. Always use the assets directory for static files, or resolve paths at runtime using `os.path` relative to your script.

Asset resolution is handled transparently. Code like `nib.Image(source="logo.png")` works in both modes without changes -- Nib resolves the path from the assets directory regardless of whether it is on disk or inside the app bundle.
