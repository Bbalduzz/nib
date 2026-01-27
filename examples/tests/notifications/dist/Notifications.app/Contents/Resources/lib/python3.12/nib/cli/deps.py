"""Dependency detection for nib build."""

import ast
import sys
from pathlib import Path
from typing import Optional


def _get_stdlib_modules() -> set[str]:
    """Get the set of standard library module names.

    Uses sys.stdlib_module_names (Python 3.10+) for accurate detection.
    """
    if hasattr(sys, "stdlib_module_names"):
        return set(sys.stdlib_module_names)
    # Fallback should never be needed (nib requires Python 3.10+)
    return set()


def _load_import_mappings() -> dict[str, str]:
    """Load import name to package name mappings.

    This handles cases where the import name differs from the pip package name.
    The mapping file can be extended by users.
    """
    # Common mappings - these are well-known discrepancies
    return {
        "PIL": "Pillow",
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "yaml": "pyyaml",
        "bs4": "beautifulsoup4",
        "dateutil": "python-dateutil",
        "dotenv": "python-dotenv",
        "jwt": "pyjwt",
        "serial": "pyserial",
        "usb": "pyusb",
        "gi": "pygobject",
        "skimage": "scikit-image",
        "cv": "opencv-python",
        "OpenGL": "pyopengl",
        "wx": "wxpython",
        "Crypto": "pycryptodome",
        "magic": "python-magic",
        "zmq": "pyzmq",
        "psycopg2": "psycopg2-binary",
    }


# Lazy-loaded module sets
_STDLIB_MODULES: Optional[set[str]] = None
_IMPORT_TO_PACKAGE: Optional[dict[str, str]] = None


def _get_stdlib() -> set[str]:
    """Get stdlib modules (cached)."""
    global _STDLIB_MODULES
    if _STDLIB_MODULES is None:
        _STDLIB_MODULES = _get_stdlib_modules()
    return _STDLIB_MODULES


def _get_mappings() -> dict[str, str]:
    """Get import mappings (cached)."""
    global _IMPORT_TO_PACKAGE
    if _IMPORT_TO_PACKAGE is None:
        _IMPORT_TO_PACKAGE = _load_import_mappings()
    return _IMPORT_TO_PACKAGE


def detect_imports(script_path: Path) -> set[str]:
    """Extract top-level imports from a Python script.

    Args:
        script_path: Path to the Python script to analyze.

    Returns:
        Set of third-party module names (excluding stdlib and nib).
    """
    source = script_path.read_text()
    tree = ast.parse(source)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    # Filter out stdlib and nib
    return filter_third_party(imports)


def filter_third_party(imports: set[str]) -> set[str]:
    """Filter out standard library and nib modules.

    Args:
        imports: Set of module names.

    Returns:
        Set of third-party module names.
    """
    stdlib = _get_stdlib()
    third_party = set()
    for module in imports:
        # Skip stdlib
        if module in stdlib:
            continue
        # Skip nib (it's bundled automatically)
        if module == "nib":
            continue
        # Skip private modules
        if module.startswith("_"):
            continue
        third_party.add(module)
    return third_party


def resolve_packages(imports: set[str]) -> list[str]:
    """Convert import names to pip package names.

    Args:
        imports: Set of import names.

    Returns:
        List of pip package names.
    """
    mappings = _get_mappings()
    packages = []
    for imp in imports:
        package = mappings.get(imp, imp)
        packages.append(package)
    return sorted(packages)


def extract_metadata(script_path: Path) -> dict[str, Optional[str]]:
    """Extract app metadata from a nib script using AST.

    Looks for patterns like:
        app.title = "My App"
        app.icon = SFSymbol("star.fill")

    Args:
        script_path: Path to the Python script.

    Returns:
        Dictionary with 'title' and 'icon' keys.
    """
    source = script_path.read_text()
    tree = ast.parse(source)

    metadata: dict[str, Optional[str]] = {"title": None, "icon": None}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                # Look for app.title = "..."
                if isinstance(target, ast.Attribute):
                    if target.attr == "title" and isinstance(node.value, ast.Constant):
                        metadata["title"] = str(node.value.value)
                    elif target.attr == "icon":
                        # Handle SFSymbol("name") or string literal
                        if isinstance(node.value, ast.Call):
                            if hasattr(node.value.func, "id"):
                                if node.value.func.id == "SFSymbol":
                                    if node.value.args and isinstance(
                                        node.value.args[0], ast.Constant
                                    ):
                                        metadata["icon"] = str(node.value.args[0].value)
                        elif isinstance(node.value, ast.Constant):
                            metadata["icon"] = str(node.value.value)

    return metadata
