"""Command-line interface for the Nib framework.

This module provides the main entry point for the ``nib`` command-line tool,
which enables developers to create, configure, and build macOS menu bar
applications written in Python.

The CLI supports two primary commands:
    - ``nib create <name>``: Scaffold a new Nib project with standard structure
    - ``nib build [script]``: Bundle a Nib application as a standalone .app

Configuration can be provided via command-line arguments or through a
``pyproject.toml`` file with a ``[tool.nib]`` section for project-level defaults.

Example:
    Creating a new project::

        $ nib create my-awesome-app
        Creating nib project: My Awesome App
          Created: src/main.py
          Created: pyproject.toml
          Created: README.md

    Building an application::

        $ nib build src/main.py --name "My App" --icon icon.png
        Using nib-runtime: /path/to/nib-runtime
        Building: My App
        Target architecture: arm64
        Detecting dependencies...
        Setting up Python runtime...
        Installing dependencies...
        Success! App bundle created at: dist/My App.app

    Using pyproject.toml configuration::

        $ cd my-project
        $ nib build  # Uses settings from pyproject.toml

Attributes:
    __all__ (list[str]): Public API exports including ``build_app``,
        ``create_project``, ``detect_imports``, ``resolve_packages``, and ``main``.

See Also:
    - :mod:`nib.cli.build`: App bundling functionality
    - :mod:`nib.cli.create`: Project scaffolding functionality
    - :mod:`nib.cli.deps`: Dependency detection utilities
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Optional

from .build import build_app
from .create import create_project
from .deps import detect_imports, resolve_packages


# Add custom SUCCESS level (between INFO and WARNING)
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


def _success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)


logging.Logger.success = _success


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output (loguru-style)."""

    # ANSI color codes
    GREY = "\033[38;5;245m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    BRIGHT_GREEN = "\033[92m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    LEVEL_COLORS = {
        "DEBUG": CYAN,
        "INFO": GREEN,
        "SUCCESS": BRIGHT_GREEN,
        "WARNING": YELLOW,
        "ERROR": RED,
        "CRITICAL": MAGENTA,
    }

    def format(self, record: logging.LogRecord) -> str:
        from datetime import datetime

        # Check if terminal supports colors
        use_colors = sys.stdout.isatty()

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.") + f"{datetime.now().microsecond // 1000:03d}"

        # Level (padded to 8 chars)
        level = record.levelname.ljust(8)

        # Module and line info
        module = record.name.split(".")[-1]  # Just the last part (e.g., "build" from "nib.build")
        func = record.funcName if record.funcName != "<module>" else "main"
        location = f"{module}:{func}:{record.lineno}"

        # Message
        message = record.getMessage()

        if use_colors:
            level_color = self.LEVEL_COLORS.get(record.levelname, "")
            return (
                f"{self.GREY}{timestamp}{self.RESET} | "
                f"{level_color}{self.BOLD}{level}{self.RESET} | "
                f"{self.CYAN}{location}{self.RESET} - {message}"
            )
        else:
            return f"{timestamp} | {level} | {location} - {message}"


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the CLI.

    Args:
        verbose: If True, enable DEBUG level logging. Otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())

    # Clear any existing handlers
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

__all__ = ["build_app", "create_project", "detect_imports", "resolve_packages", "main"]


def load_pyproject_config() -> Optional[dict[str, Any]]:
    """Load Nib configuration from pyproject.toml in the current directory.

    Searches for a ``pyproject.toml`` file in the current working directory
    and extracts the ``[tool.nib]`` section if present, along with project
    dependencies from ``[project].dependencies``. This allows users to
    define project-level defaults for build settings, entry points, and
    application metadata.

    The function attempts to use ``tomllib`` (Python 3.11+) or falls back to
    ``tomli`` for older Python versions. If neither is available, returns None.

    Returns:
        dict[str, Any] | None: A dictionary containing the Nib configuration
            from ``[tool.nib]`` section, or None if:
            - No pyproject.toml exists in the current directory
            - No tomllib/tomli parser is available
            - The file cannot be parsed
            - No ``[tool.nib]`` section exists

            The returned dict also includes a ``_project_dependencies`` key
            with the list of dependencies from ``[project].dependencies``.

    Example:
        Configuration in pyproject.toml::

            [project]
            dependencies = ["requests", "pillow"]

            [tool.nib]
            entry = "src/main.py"

            [tool.nib.build]
            name = "My App"
            identifier = "com.example.myapp"
            version = "1.0.0"
            icon = "src/assets/icon.png"

        Loading the configuration::

            >>> config = load_pyproject_config()
            >>> config.get("entry")
            'src/main.py'
            >>> config.get("build", {}).get("name")
            'My App'
            >>> config.get("_project_dependencies")
            ['requests', 'pillow']
    """
    pyproject_path = Path.cwd() / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    try:
        import tomllib
    except ImportError:
        # Python < 3.11
        try:
            import tomli as tomllib
        except ImportError:
            return None

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
        nib_config = data.get("tool", {}).get("nib", {})
        # Also extract project dependencies
        project_deps = data.get("project", {}).get("dependencies", [])
        # Parse dependency strings to extract package names (strip version specs)
        parsed_deps = []
        for dep in project_deps:
            # Handle "package>=1.0" or "package[extra]>=1.0" formats
            name = dep.split("[")[0].split("<")[0].split(">")[0].split("=")[0].split("!")[0].strip()
            if name and name.lower() != "nib":  # Exclude nib itself
                parsed_deps.append(name)
        nib_config["_project_dependencies"] = parsed_deps
        return nib_config
    except Exception:
        return None


def main() -> int:
    """Main entry point for the Nib command-line interface.

    Parses command-line arguments and dispatches to the appropriate subcommand
    handler. Supports the following commands:

    Commands:
        create: Create a new Nib project with standard directory structure,
            including ``src/main.py``, ``pyproject.toml``, and ``README.md``.

        build: Build a standalone macOS ``.app`` bundle from a Nib script.
            Can use settings from ``pyproject.toml`` or command-line arguments.

    The build command merges configuration from multiple sources with the
    following precedence (highest to lowest):
        1. Command-line arguments
        2. ``[tool.nib.build]`` section in pyproject.toml
        3. Default values

    Returns:
        int: Exit code where 0 indicates success and non-zero indicates failure.
            - 0: Command completed successfully
            - 1: Error occurred (missing file, build failure, etc.)

    Example:
        Running from command line::

            $ nib create myapp      # Create new project
            $ nib build             # Build using pyproject.toml
            $ nib build app.py      # Build specific script
            $ nib --help            # Show help

        Programmatic usage::

            >>> import sys
            >>> sys.argv = ['nib', 'create', 'myapp']
            >>> exit_code = main()
            >>> print(f"Exited with code: {exit_code}")

    Note:
        This function is typically invoked via the ``nib`` console script
        entry point defined in the package's setup configuration.
    """
    parser = argparse.ArgumentParser(
        prog="nib",
        description="Nib - Build macOS menu bar apps with Python",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new nib project",
        description="Create a new nib project with standard structure.",
    )
    create_parser.add_argument(
        "name",
        help="Project name",
    )

    # Build command
    build_parser = subparsers.add_parser(
        "build",
        help="Build a standalone .app bundle",
        description="Build a standalone macOS .app bundle. Uses pyproject.toml if present.",
    )
    build_parser.add_argument(
        "script",
        type=Path,
        nargs="?",
        help="Python script to bundle (default: from pyproject.toml)",
    )
    build_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (default: ./dist/)",
    )
    build_parser.add_argument(
        "-n", "--name",
        help="App name (default: from pyproject.toml or script name)",
    )
    build_parser.add_argument(
        "-i", "--icon",
        type=Path,
        help="Icon file (.icns or .png)",
    )
    build_parser.add_argument(
        "--identifier",
        help="Bundle identifier (default: com.nib.<name>)",
    )
    build_parser.add_argument(
        "--version",
        help="App version (default: from pyproject.toml or 1.0.0)",
    )
    build_parser.add_argument(
        "--extra-deps",
        help="Additional pip packages (comma-separated)",
    )
    build_parser.add_argument(
        "--min-macos",
        help="Minimum macOS version (default: current)",
    )
    build_parser.add_argument(
        "--exclude",
        help="Packages to exclude from bundling (comma-separated)",
    )
    build_parser.add_argument(
        "--arch",
        choices=["arm64", "x86_64"],
        help="Target architecture (default: current machine)",
    )
    build_parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Keep Python source files (skip bytecode compilation)",
    )
    build_parser.add_argument(
        "--obfuscate",
        action="store_true",
        help="Apply real obfuscation via pyc-zipper (implies compilation)",
    )

    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a nib app with hot reload",
        description="Run a Nib application with automatic reload on file changes.",
    )
    run_parser.add_argument(
        "script",
        type=Path,
        nargs="?",
        help="Python script to run (default: from pyproject.toml)",
    )
    run_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Watch subdirectories for changes",
    )

    args = parser.parse_args()

    # Configure logging
    setup_logging(verbose=getattr(args, "verbose", False))
    logger = logging.getLogger("nib.cli")

    if args.command == "create":
        return create_project(name=args.name)

    elif args.command == "build":
        # Load config from pyproject.toml
        config = load_pyproject_config() or {}
        build_config = config.get("build", {})

        # Determine script path
        script = args.script
        if script is None:
            entry = config.get("entry", "src/main.py")
            script = Path(entry)
            if not script.exists():
                logger.error(f"Entry point not found: {script}")
                logger.error("Specify a script or create pyproject.toml with [tool.nib] entry")
                return 1

        # Merge CLI args with config (CLI takes precedence)
        output = args.output or Path(build_config.get("output", "dist"))
        name = args.name or build_config.get("name")
        icon = args.icon
        if icon is None and "icon" in build_config:
            icon = Path(build_config["icon"])
        # Default icon location (check for .icns first, then .png)
        if icon is None:
            for icon_name in ["icon.icns", "icon.png"]:
                default_icon = Path("src/assets") / icon_name
                if default_icon.exists():
                    icon = default_icon
                    break

        identifier = args.identifier or build_config.get("identifier")
        version = args.version or build_config.get("version", "1.0.0")
        extra_deps = args.extra_deps or build_config.get("extra_deps")
        if isinstance(extra_deps, list):
            extra_deps = ",".join(extra_deps)
        min_macos = args.min_macos or build_config.get("min_macos")
        excludes = args.exclude or build_config.get("exclude")
        if isinstance(excludes, list):
            excludes = ",".join(excludes)

        # Get plist options from config
        plist_options = build_config.get("plist", {})

        # Get explicit dependencies from [project].dependencies
        project_deps = config.get("_project_dependencies", [])

        # Get arch from CLI or config
        arch = args.arch or build_config.get("arch")

        # Launch at login setting
        launch_at_login = build_config.get("launch_at_login", False)

        # Compilation setting (default: True, can be disabled via CLI or config)
        no_compile = args.no_compile or not build_config.get("compile", True)

        # Obfuscation setting (default: False, can be enabled via CLI or config)
        obfuscate = args.obfuscate or build_config.get("obfuscate", False)

        # Validate: can't obfuscate without compiling
        if obfuscate and no_compile:
            logger.error("Cannot use --obfuscate with --no-compile")
            return 1

        return build_app(
            script=script,
            name=name,
            output=output,
            icon=icon,
            identifier=identifier,
            version=version,
            extra_deps=extra_deps,
            min_macos=min_macos,
            excludes=excludes,
            plist_options=plist_options,
            explicit_deps=project_deps if project_deps else None,
            arch=arch,
            launch_at_login=launch_at_login,
            no_compile=no_compile,
            obfuscate=obfuscate,
        )

    elif args.command == "run":
        from .run import run_with_reload

        # Determine script path
        script = args.script
        if script is None:
            config = load_pyproject_config() or {}
            entry = config.get("entry", "src/main.py")
            script = Path(entry)
            if not script.exists():
                logger.error(f"Entry point not found: {script}")
                logger.error("Specify a script or create pyproject.toml with [tool.nib] entry")
                return 1

        if not script.exists():
            logger.error(f"Script not found: {script}")
            return 1

        # If script is a directory, look for src/main.py inside it
        recursive = args.recursive
        if script.is_dir():
            project_dir = script
            main_file = project_dir / "src" / "main.py"
            if not main_file.exists():
                logger.error(f"No src/main.py found in {project_dir}")
                return 1
            script = main_file
            # Enable recursive watching for project directories
            recursive = True

        return run_with_reload(script, recursive=recursive)

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
