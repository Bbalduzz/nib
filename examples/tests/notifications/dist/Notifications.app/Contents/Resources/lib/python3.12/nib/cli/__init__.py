"""Nib CLI for building macOS app bundles."""

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

from .build import build_app
from .create import create_project
from .deps import detect_imports, resolve_packages

__all__ = ["build_app", "create_project", "detect_imports", "resolve_packages", "main"]


def load_pyproject_config() -> Optional[dict[str, Any]]:
    """Load nib config from pyproject.toml in current directory.

    Returns:
        Config dict or None if not found.
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
        return data.get("tool", {}).get("nib", {})
    except Exception:
        return None


def main() -> int:
    """Main entry point for the nib CLI."""
    parser = argparse.ArgumentParser(
        prog="nib",
        description="Nib - Build macOS menu bar apps with Python",
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

    args = parser.parse_args()

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
                print(f"Error: Entry point not found: {script}")
                print("Specify a script or create pyproject.toml with [tool.nib] entry")
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
        )
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
