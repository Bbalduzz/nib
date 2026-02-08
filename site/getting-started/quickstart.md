# Quick Start

This page gets you from zero to a running menu bar app in under a minute.

## Create a new project

Use the `nib create` command to scaffold a project:

```bash
nib create myapp
```

You will see output like:

```
Creating nib project: Myapp
  Created: src/main.py
  Created: pyproject.toml
  Created: README.md
  Created: src/assets/

Project created at: /path/to/myapp

Next steps:
  cd myapp
  python src/main.py    # Run in development
  nib build             # Build standalone app
```

## What gets generated

The scaffolded project has the following layout:

```
myapp/
├── src/
│   ├── main.py          # Application entry point
│   └── assets/          # Icons, images, fonts
├── pyproject.toml       # Project metadata and Nib build config
└── README.md            # Basic documentation
```

### src/main.py

The generated entry point is a counter app that demonstrates the core concepts -- app configuration, views, reactivity, and a context menu:

```python
"""
Myapp - A nib application
"""

import nib


def main(app: nib.App):
    app.title = "Myapp"
    app.icon = nib.SFSymbol("star.fill")
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    counter = nib.Text("0")

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Hello, Myapp!", font=nib.Font.title),
                counter,
                nib.Button("Click me", action=increment),
            ],
            spacing=16,
            padding=24,
        )
    )


nib.run(main)
```

### pyproject.toml

The generated `pyproject.toml` contains project metadata and Nib build configuration. Most options are commented out with sensible defaults:

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "Myapp - A nib application"
requires-python = ">=3.10"
dependencies = [
    "nib",
]

[tool.nib]
entry = "src/main.py"

[tool.nib.build]
name = "Myapp"
# identifier = "com.example.myapp"
# version = "1.0.0"
# icon = "src/assets/icon.png"
```

## Run the app

Navigate into the project directory and launch it with `nib run`:

```bash
cd myapp
nib run src/main.py
```

A new icon appears in your macOS menu bar. Click it to open the popover and see your app. Every time you save a `.py` file, Nib hot-reloads the application automatically.

!!! tip
    Use the `-r` flag to watch subdirectories recursively for changes:
    ```bash
    nib run src/main.py -r
    ```

## What just happened

When you run `nib run`, the following happens:

1. **Python** starts your script and builds the view tree.
2. **Swift runtime** launches as a separate process, creating a native macOS menu bar app.
3. The two processes connect over a **Unix socket** using MessagePack serialization.
4. Python sends the full view tree to Swift, which renders it as native SwiftUI.
5. **Watchdog** monitors your files and reloads the Python side on every save, keeping the Swift runtime alive.

## Next steps

- [Your First App](first-app.md) -- Build an app from scratch to understand every piece.
- [Project Structure](project-structure.md) -- Learn about assets, fonts, and build configuration.
