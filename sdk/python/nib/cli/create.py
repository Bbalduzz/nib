"""Project scaffolding for new Nib applications.

This module provides functionality to create new Nib projects with a standard
directory structure and boilerplate files. It generates a complete project
skeleton that developers can immediately run and customize.

The generated project structure includes:
    - ``src/main.py``: Main application entry point with example code
    - ``src/assets/``: Directory for icons, images, and other resources
    - ``pyproject.toml``: Project configuration with Nib build settings
    - ``README.md``: Basic documentation with development instructions

Example:
    Creating a project from the command line::

        $ nib create my-awesome-app
        Creating nib project: My Awesome App
          Created: src/main.py
          Created: pyproject.toml
          Created: README.md
          Created: src/assets/

        Project created at: /path/to/my_awesome_app

        Next steps:
          cd my_awesome_app
          python src/main.py    # Run in development
          nib build             # Build standalone app

    Creating a project programmatically::

        >>> from nib.cli.create import create_project
        >>> from pathlib import Path
        >>> exit_code = create_project("My App", path=Path("/projects"))
        Creating nib project: My App
        ...
        >>> exit_code
        0

Attributes:
    MAIN_PY_TEMPLATE (str): Template for the main.py entry point file.
        Contains a basic Nib application with a counter example.

    PYPROJECT_TEMPLATE (str): Template for pyproject.toml with project
        metadata and Nib build configuration options (commented).

    README_TEMPLATE (str): Template for README.md with development and
        build instructions.

See Also:
    - :func:`nib.cli.build.build_app`: Build the created project into an app
    - :mod:`nib.cli`: Main CLI module for command handling
"""

import os
from pathlib import Path
from typing import Optional

from ..core.logging import logger

MAIN_PY_TEMPLATE = '''"""
{name} - A nib application
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

# Start app automatically at login (requires signed app)
# launch_at_login = false

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
    """Create a new Nib project with standard directory structure.

    Generates a complete project skeleton for a Nib macOS menu bar application,
    including source files, configuration, and documentation. The project is
    immediately runnable and can be built into a standalone .app bundle.

    The project name is normalized in two ways:
        - Display name: Title-cased with spaces (e.g., "My Awesome App")
        - Directory name: Lowercase with underscores (e.g., "my_awesome_app")

    Args:
        name (str): Project name. Can contain spaces, hyphens, or underscores.
            Will be normalized to create both a display name and a directory name.
            Examples: "my-app", "My App", "my_awesome_app"

        path (Path | None): Parent directory where the project folder will be
            created. Defaults to the current working directory if not specified.
            The actual project will be created in a subdirectory named after
            the normalized project name.

    Returns:
        int: Exit code indicating success or failure.
            - 0: Project created successfully
            - 1: Error occurred (e.g., directory already exists)

    Raises:
        No exceptions are raised; errors are printed to stdout and
        indicated via the return code.

    Example:
        Basic usage::

            >>> exit_code = create_project("My App")
            Creating nib project: My App
              Created: src/main.py
              Created: pyproject.toml
              Created: README.md
              Created: src/assets/

            Project created at: /current/dir/my_app

            Next steps:
              cd my_app
              python src/main.py    # Run in development
              nib build             # Build standalone app
            >>> exit_code
            0

        Specifying a custom path::

            >>> exit_code = create_project("widget", path=Path("/projects"))
            >>> # Creates /projects/widget/

        Handling existing directory::

            >>> exit_code = create_project("existing_project")
            Error: Directory already exists: /path/to/existing_project
            >>> exit_code
            1

    Note:
        The generated ``pyproject.toml`` contains commented configuration
        options that users can uncomment and customize for their needs,
        including bundle identifier, icon path, and Info.plist settings.
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
        logger.error(f"Directory already exists: {project_dir}")
        return 1

    logger.info(f"Creating nib project: {name_display}")

    # Create directory structure
    (project_dir / "src" / "assets").mkdir(parents=True)

    # Create main.py
    main_py = project_dir / "src" / "main.py"
    main_py.write_text(MAIN_PY_TEMPLATE.format(name=name_display))
    logger.info("Created: src/main.py")

    # Create pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    pyproject.write_text(
        PYPROJECT_TEMPLATE.format(
            name=name_display,
            name_lower=name_lower,
        )
    )
    logger.info("Created: pyproject.toml")

    # Create README.md
    readme = project_dir / "README.md"
    readme.write_text(README_TEMPLATE.format(name=name_display))
    logger.info("Created: README.md")

    # Create placeholder for icon
    assets_readme = project_dir / "src" / "assets" / ".gitkeep"
    assets_readme.write_text("# Place your icon.png here\n")
    logger.info("Created: src/assets/")

    logger.success(f"Project created at: {project_dir}")
    logger.info("Next steps:")
    logger.info(f"  cd {name_lower}")
    logger.info("  python src/main.py    # Run in development")
    logger.info("  nib build             # Build standalone app")

    return 0
