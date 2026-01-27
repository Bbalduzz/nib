"""Create new nib project scaffolding."""

import os
from pathlib import Path
from typing import Optional

MAIN_PY_TEMPLATE = '''"""
{name} - A nib application

Assets:
    Place images, videos, and other files in src/assets/
    Then use them with relative paths:
        nib.Image("logo.png")           -> src/assets/logo.png
        nib.Image("images/icon.png")    -> src/assets/images/icon.png
"""

import nib


def main(app: nib.App):
    app.title = "{name}"
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
                nib.Text("Hello, {name}!", font=nib.Font.title),
                counter,
                nib.Button("Click me", action=increment),
            ],
            spacing=16,
            padding=24,
        )
    )


nib.run(main)
'''


PYPROJECT_TEMPLATE = """[project]
name = "{name_lower}"
version = "0.1.0"
description = "{name} - A nib application"
requires-python = ">=3.10"
dependencies = [
    "nib",
]

[tool.nib]
# Entry point for the application
entry = "src/main.py"

[tool.nib.build]
# App display name (defaults to project name)
name = "{name}"

# Bundle identifier (defaults to com.nib.<name>)
# identifier = "com.example.{name_lower}"

# App version (defaults to project version)
# version = "1.0.0"

# Icon file (defaults to src/assets/icon.png if exists)
# icon = "src/assets/icon.png"

# Minimum macOS version (defaults to current)
# min_macos = "14.0"

# Additional packages to exclude from bundling
# exclude = []

# Additional dependencies to include (if auto-detection misses them)
# extra_deps = []

# Info.plist options
# [tool.nib.build.plist]
# copyright = "Copyright © 2025 Your Name"
# category = "public.app-category.utilities"
# notification_style = "banner"  # "banner", "alert", or "none"
# url_schemes = ["myapp"]

# Privacy usage descriptions
# [tool.nib.build.plist.usage]
# microphone = "This app needs microphone access for..."
# camera = "This app needs camera access for..."
# location = "This app needs location access for..."
# apple_events = "This app needs to control other apps for..."

# Custom plist keys
# [tool.nib.build.plist.custom]
# MyCustomKey = "value"
"""


README_TEMPLATE = """# {name}

A macOS menu bar application built with [nib](https://github.com/Bbalduzz/nib).

## Development

Run the app in development mode:

```bash
python src/main.py
```

## Building

Build a standalone `.app` bundle:

```bash
nib build
```

The app will be created in `dist/{name}.app`.
"""


def create_project(
    name: str,
    path: Optional[Path] = None,
) -> int:
    """Create a new nib project.

    Args:
        name: Project name.
        path: Directory to create project in (default: current directory).

    Returns:
        Exit code (0 for success).
    """
    # Normalize name
    name_display = name.replace("_", " ").replace("-", " ").title()
    name_lower = name.lower().replace(" ", "_").replace("-", "_")

    # Determine project path
    if path is None:
        path = Path.cwd()
    project_dir = path / name_lower

    # Check if directory already exists
    if project_dir.exists():
        print(f"Error: Directory already exists: {project_dir}")
        return 1

    print(f"Creating nib project: {name_display}")

    # Create directory structure
    (project_dir / "src" / "assets").mkdir(parents=True)

    # Create main.py
    main_py = project_dir / "src" / "main.py"
    main_py.write_text(MAIN_PY_TEMPLATE.format(name=name_display))
    print(f"  Created: src/main.py")

    # Create pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    pyproject.write_text(
        PYPROJECT_TEMPLATE.format(
            name=name_display,
            name_lower=name_lower,
        )
    )
    print(f"  Created: pyproject.toml")

    # Create README.md
    readme = project_dir / "README.md"
    readme.write_text(README_TEMPLATE.format(name=name_display))
    print(f"  Created: README.md")

    # Create placeholder for icon
    assets_readme = project_dir / "src" / "assets" / ".gitkeep"
    assets_readme.write_text("# Place your icon.png here\n")
    print(f"  Created: src/assets/")

    print(f"\nProject created at: {project_dir}")
    print(f"\nNext steps:")
    print(f"  cd {name_lower}")
    print(f"  python src/main.py    # Run in development")
    print(f"  nib build             # Build standalone app")

    return 0
