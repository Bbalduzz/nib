"""Dependency detection and resolution for Nib application bundling.

This module provides utilities for analyzing Python source files to detect
third-party dependencies and convert them to pip package names. It uses
AST (Abstract Syntax Tree) analysis for accurate import detection without
executing the code.

The module handles several challenges in dependency detection:

    1. **Standard Library Filtering**: Uses ``sys.stdlib_module_names`` to
       accurately identify and exclude Python standard library modules.

    2. **Import Name Mapping**: Handles cases where the import name differs
       from the pip package name (e.g., ``PIL`` -> ``Pillow``).

    3. **Metadata Extraction**: Extracts app configuration (title, icon) from
       the source code without executing it.

Example:
    Detecting dependencies in a script::

        >>> from nib.cli.deps import detect_imports, resolve_packages
        >>> from pathlib import Path
        >>> imports = detect_imports(Path("myapp.py"))
        >>> imports
        {'requests', 'numpy', 'PIL'}
        >>> packages = resolve_packages(imports)
        >>> packages
        ['numpy', 'Pillow', 'requests']

    Extracting app metadata::

        >>> from nib.cli.deps import extract_metadata
        >>> metadata = extract_metadata(Path("myapp.py"))
        >>> metadata
        {'title': 'My App', 'icon': 'star.fill'}

Workflow:
    1. ``detect_imports(script)`` - Parse script and extract import names
    2. ``filter_third_party(imports)`` - Remove stdlib and nib imports
    3. ``resolve_packages(imports)`` - Map import names to pip packages

Attributes:
    _STDLIB_MODULES (set[str] | None): Cached set of standard library
        module names. Populated lazily on first use.

    _IMPORT_TO_PACKAGE (dict[str, str] | None): Cached mapping of import
        names to pip package names. Populated lazily on first use.

See Also:
    - :mod:`nib.cli.build`: Uses this module for dependency detection
    - :mod:`ast`: Python's Abstract Syntax Tree module
"""

import ast
import sys
from pathlib import Path
from typing import Optional


def _get_stdlib_modules() -> set[str]:
    """Get the complete set of Python standard library module names.

    Uses ``sys.stdlib_module_names`` (available in Python 3.10+) for accurate
    and complete detection of all standard library modules. This is more
    reliable than maintaining a manual list.

    Returns:
        set[str]: A set of all standard library module names. Returns an
            empty set if ``sys.stdlib_module_names`` is not available
            (should not happen as Nib requires Python 3.10+).

    Example:
        >>> stdlib = _get_stdlib_modules()
        >>> "os" in stdlib
        True
        >>> "json" in stdlib
        True
        >>> "requests" in stdlib
        False

    Note:
        This is an internal function. Use :func:`detect_imports` or
        :func:`filter_third_party` for public API access.
    """
    if hasattr(sys, "stdlib_module_names"):
        return set(sys.stdlib_module_names)
    # Fallback should never be needed (nib requires Python 3.10+)
    return set()


def _load_import_mappings() -> dict[str, str]:
    """Load the mapping of Python import names to pip package names.

    Many popular packages have import names that differ from their pip package
    names. This function returns a dictionary of known mappings to ensure
    correct package resolution during bundling.

    Returns:
        dict[str, str]: Dictionary mapping import names (keys) to pip package
            names (values). All mappings are for well-known packages where
            the import name differs from the package name.

    Example:
        >>> mappings = _load_import_mappings()
        >>> mappings["PIL"]
        'Pillow'
        >>> mappings["cv2"]
        'opencv-python'
        >>> mappings["yaml"]
        'pyyaml'

    Currently Supported Mappings:
        - PIL -> Pillow
        - cv2, cv -> opencv-python
        - sklearn -> scikit-learn
        - yaml -> pyyaml
        - bs4 -> beautifulsoup4
        - dateutil -> python-dateutil
        - dotenv -> python-dotenv
        - jwt -> pyjwt
        - serial -> pyserial
        - usb -> pyusb
        - gi -> pygobject
        - skimage -> scikit-image
        - OpenGL -> pyopengl
        - wx -> wxpython
        - Crypto -> pycryptodome
        - magic -> python-magic
        - zmq -> pyzmq
        - psycopg2 -> psycopg2-binary

    Note:
        This is an internal function. If an import is not in this mapping,
        :func:`resolve_packages` assumes the import name equals the package
        name, which is correct for most packages.
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
    """Get standard library module names with caching.

    Returns the cached set of stdlib modules, populating the cache on first
    call. This avoids repeated computation when processing multiple files.

    Returns:
        set[str]: Cached set of standard library module names.
    """
    global _STDLIB_MODULES
    if _STDLIB_MODULES is None:
        _STDLIB_MODULES = _get_stdlib_modules()
    return _STDLIB_MODULES


def _get_mappings() -> dict[str, str]:
    """Get import-to-package name mappings with caching.

    Returns the cached mapping dictionary, populating the cache on first
    call. This avoids repeated computation when resolving multiple imports.

    Returns:
        dict[str, str]: Cached mapping of import names to pip package names.
    """
    global _IMPORT_TO_PACKAGE
    if _IMPORT_TO_PACKAGE is None:
        _IMPORT_TO_PACKAGE = _load_import_mappings()
    return _IMPORT_TO_PACKAGE


def detect_imports(script_path: Path) -> set[str]:
    """Extract third-party imports from a Python script using AST analysis.

    Parses the Python source file and extracts all import statements,
    filtering out standard library modules and the nib package itself.
    Uses AST analysis to avoid executing the code.

    Handles both import styles:
        - ``import module`` statements
        - ``from module import ...`` statements

    For dotted imports (e.g., ``from package.submodule import func``), only
    the top-level package name is extracted.

    Args:
        script_path (Path): Path to the Python script to analyze. The file
            must be valid Python syntax.

    Returns:
        set[str]: Set of third-party module/package names found in the script.
            Standard library modules and ``nib`` are excluded.

    Raises:
        SyntaxError: If the script contains invalid Python syntax.
        FileNotFoundError: If the script file does not exist.

    Example:
        Given a script with these imports::

            import os
            import json
            import requests
            from PIL import Image
            from nib import App

        The function returns::

            >>> imports = detect_imports(Path("script.py"))
            >>> imports
            {'requests', 'PIL'}

        Note that ``os``, ``json`` (stdlib) and ``nib`` are excluded.

    See Also:
        - :func:`resolve_packages`: Convert import names to pip package names
        - :func:`filter_third_party`: Filter out non-third-party imports
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
    """Filter a set of imports to keep only third-party packages.

    Removes standard library modules, the nib package, and private modules
    (those starting with underscore) from the input set.

    Args:
        imports (set[str]): Set of module/package names to filter.

    Returns:
        set[str]: Filtered set containing only third-party package names.
            The following are excluded:
            - Standard library modules (os, json, asyncio, etc.)
            - The ``nib`` package (bundled automatically)
            - Private modules (names starting with ``_``)

    Example:
        >>> imports = {"os", "requests", "nib", "PIL", "_internal", "json"}
        >>> third_party = filter_third_party(imports)
        >>> third_party
        {'requests', 'PIL'}

    Note:
        This function is called internally by :func:`detect_imports` but
        can also be used independently to filter arbitrary import sets.
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
    """Convert Python import names to pip package names.

    Maps import names to their corresponding pip package names using the
    known mappings from :func:`_load_import_mappings`. For imports not in
    the mapping, assumes the import name equals the package name.

    Args:
        imports (set[str]): Set of Python import/module names as they
            appear in import statements.

    Returns:
        list[str]: Sorted list of pip package names suitable for installation
            or bundling. Duplicates are not possible since input is a set.

    Example:
        >>> imports = {"requests", "PIL", "yaml", "numpy"}
        >>> packages = resolve_packages(imports)
        >>> packages
        ['numpy', 'Pillow', 'pyyaml', 'requests']

        Note that:
        - ``PIL`` is mapped to ``Pillow``
        - ``yaml`` is mapped to ``pyyaml``
        - ``requests`` and ``numpy`` are unchanged (import == package)
        - Result is sorted alphabetically

    See Also:
        - :func:`detect_imports`: Extract imports from a script
        - :func:`_load_import_mappings`: View/extend the mapping dictionary
    """
    mappings = _get_mappings()
    packages = []
    for imp in imports:
        package = mappings.get(imp, imp)
        packages.append(package)
    return sorted(packages)


def extract_metadata(script_path: Path) -> dict[str, Optional[str]]:
    """Extract application metadata from a Nib script using AST analysis.

    Parses the Python source file and looks for common Nib app configuration
    patterns to extract the application title and icon. This allows the build
    system to use sensible defaults without requiring explicit configuration.

    Recognized patterns:
        - ``app.title = "My App"`` - Extracts the title string
        - ``app.icon = SFSymbol("star.fill")`` - Extracts the SF Symbol name
        - ``app.icon = "icon.png"`` - Extracts the icon path/name

    Args:
        script_path (Path): Path to the Nib Python script to analyze.

    Returns:
        dict[str, str | None]: Dictionary with extracted metadata:
            - ``title`` (str | None): Application title if found
            - ``icon`` (str | None): Icon name or SF Symbol name if found

            Both values are None if the corresponding pattern was not found.

    Raises:
        SyntaxError: If the script contains invalid Python syntax.
        FileNotFoundError: If the script file does not exist.

    Example:
        Given a script containing::

            def main(app: nib.App):
                app.title = "My Awesome App"
                app.icon = nib.SFSymbol("star.fill")
                ...

        The function extracts::

            >>> metadata = extract_metadata(Path("myapp.py"))
            >>> metadata
            {'title': 'My Awesome App', 'icon': 'star.fill'}

        For a script without these assignments::

            >>> metadata = extract_metadata(Path("minimal.py"))
            >>> metadata
            {'title': None, 'icon': None}

    Note:
        This function uses AST analysis and does not execute the script.
        It only detects simple assignment patterns and may not find
        dynamically computed values.
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
