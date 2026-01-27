"""Build standalone macOS app bundles from Nib scripts.

This module provides functionality to bundle Nib applications as standalone
macOS ``.app`` bundles using py2app. It handles the complete build pipeline:

    - Automatic dependency detection from Python imports
    - Icon conversion (PNG to ICNS format)
    - Info.plist generation with configurable metadata
    - Swift runtime (nib-runtime) bundling
    - Asset directory copying

The build process creates a self-contained application that can be distributed
without requiring Python or any dependencies to be installed on the target system.

Build Pipeline:
    1. Locate the nib-runtime Swift executable
    2. Extract app metadata (title, icon) from the script
    3. Detect third-party dependencies via AST analysis
    4. Convert icon to ICNS format if needed
    5. Generate py2app setup.py with proper configuration
    6. Run py2app to create the .app bundle
    7. Inject nib-runtime into the bundle
    8. Copy assets directory if present

Example:
    Building from command line::

        $ nib build myapp.py --name "My App" --icon icon.png
        Using nib-runtime: /path/to/nib-runtime
        Building: My App
        Detecting dependencies...
          Dependencies: requests, numpy
        Running py2app...
        Bundled nib-runtime: dist/My App.app/Contents/Resources/nib-runtime
        Success! App bundle created at: dist/My App.app
        Bundle size: 45.2 MB

    Building programmatically::

        >>> from nib.cli.build import build_app
        >>> from pathlib import Path
        >>> exit_code = build_app(
        ...     script=Path("src/main.py"),
        ...     name="My App",
        ...     icon=Path("icon.png"),
        ...     version="1.0.0",
        ... )
        >>> exit_code
        0

Configuration via pyproject.toml:
    The build command integrates with ``[tool.nib.build]`` settings::

        [tool.nib.build]
        name = "My App"
        identifier = "com.example.myapp"
        version = "1.0.0"
        icon = "src/assets/icon.png"
        min_macos = "13.0"

        [tool.nib.build.plist]
        copyright = "Copyright 2024"
        category = "public.app-category.utilities"

Requirements:
    - macOS (uses native tools: sips, iconutil)
    - py2app package installed
    - nib-runtime Swift binary built

See Also:
    - :mod:`nib.cli.deps`: Dependency detection utilities
    - :mod:`nib.cli.create`: Project scaffolding
    - :func:`nib.cli.main`: CLI entry point
"""

import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from .deps import detect_imports, extract_metadata, resolve_packages


def find_nib_runtime() -> Optional[Path]:
    """Find the nib-runtime Swift executable.

    Searches for the nib-runtime binary in multiple locations with the
    following priority order:

        1. ``NIB_RUNTIME`` environment variable (explicit path)
        2. Relative to this file (development: ``swift/.build/release/``)
        3. Relative to current directory (``swift/.build/release/``)
        4. System locations (``/usr/local/bin/``, ``~/.local/bin/``)
        5. System PATH

    Returns:
        Path | None: Absolute path to the nib-runtime executable if found,
            or None if not found in any searched location.

    Example:
        >>> runtime = find_nib_runtime()
        >>> if runtime:
        ...     print(f"Found runtime at: {runtime}")
        ... else:
        ...     print("Runtime not found - build Swift code first")
        Found runtime at: /path/to/nib/swift/.build/release/nib-runtime

    Note:
        For development, build the runtime with::

            cd swift && swift build -c release

        For production, set the ``NIB_RUNTIME`` environment variable to
        the path of the installed binary.
    """
    # Check environment variable first
    env_runtime = os.environ.get("NIB_RUNTIME")
    if env_runtime:
        path = Path(env_runtime)
        if path.exists() and path.is_file():
            return path

    # Check relative to this file (development)
    # Path(__file__) = .../nib/python/nib/cli/build.py
    # .parent.parent.parent.parent.parent = .../nib
    nib_root = Path(__file__).parent.parent.parent.parent.parent
    locations = [
        nib_root / "swift" / ".build" / "release" / "nib-runtime",
        nib_root / "swift" / ".build" / "debug" / "nib-runtime",
        Path.cwd() / "swift" / ".build" / "release" / "nib-runtime",
        Path.cwd() / "swift" / ".build" / "debug" / "nib-runtime",
        Path("/usr/local/bin/nib-runtime"),
        Path.home() / ".local" / "bin" / "nib-runtime",
    ]

    for path in locations:
        if path.exists() and path.is_file():
            return path

    # Check PATH
    path_runtime = shutil.which("nib-runtime")
    if path_runtime:
        return Path(path_runtime)

    return None


def get_installed_packages() -> set[str]:
    """Get the names of all installed Python packages.

    Uses ``importlib.metadata.distributions()`` to enumerate all installed
    packages in the current Python environment. Package names are normalized
    to lowercase with hyphens replaced by underscores for consistent comparison.

    Returns:
        set[str]: A set of normalized package names (lowercase, underscores).
            Returns an empty set if importlib.metadata is not available.

    Example:
        >>> packages = get_installed_packages()
        >>> "requests" in packages
        True
        >>> "numpy" in packages
        True
    """
    try:
        from importlib.metadata import distributions
        return {dist.metadata["Name"].lower().replace("-", "_") for dist in distributions()}
    except ImportError:
        return set()


def get_packages_to_exclude(needed: set[str]) -> list[str]:
    """Determine which installed packages should be excluded from bundling.

    Compares the set of needed packages against all installed packages to
    generate an exclusion list for py2app. This helps minimize bundle size
    by excluding unnecessary packages that happen to be installed in the
    development environment.

    Args:
        needed (set[str]): Set of package names that must be included in
            the bundle. Names should be normalized (lowercase, underscores).

    Returns:
        list[str]: Sorted list of package names to exclude from bundling.
            These are packages that are installed but not required by the app.

    Example:
        >>> needed = {"requests", "numpy", "nib", "msgpack"}
        >>> excludes = get_packages_to_exclude(needed)
        >>> "pytest" in excludes  # If pytest is installed but not needed
        True
        >>> "requests" in excludes
        False
    """
    installed = get_installed_packages()
    needed_lower = {p.lower().replace("-", "_") for p in needed}

    # Exclude everything installed except what we need
    excludes = []
    for pkg in installed:
        if pkg not in needed_lower:
            excludes.append(pkg)

    return sorted(excludes)


def get_macos_version() -> str:
    """Get the current macOS version for LSMinimumSystemVersion.

    Retrieves the running macOS version and formats it for use in
    Info.plist's ``LSMinimumSystemVersion`` key. Returns only the major
    version with ".0" suffix (e.g., "14.0" for macOS 14.2.1).

    Returns:
        str: macOS version string in "major.0" format suitable for
            LSMinimumSystemVersion. Falls back to "13.0" (Ventura)
            if the version cannot be determined.

    Example:
        >>> version = get_macos_version()
        >>> version  # Running on macOS 14.2.1
        '14.0'
    """
    import platform
    version = platform.mac_ver()[0]
    if version:
        # Use major.minor (e.g., "14.0" from "14.2.1")
        parts = version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.0"
    return "13.0"  # Fallback to Ventura


def build_plist_dict(
    name: str,
    identifier: str,
    version: str,
    min_macos: str,
    plist_options: dict,
) -> dict:
    """Build the Info.plist dictionary for the macOS app bundle.

    Constructs a complete Info.plist configuration dictionary with standard
    macOS bundle keys and optional customizations. The generated plist
    configures the app as an LSUIElement (menu bar only, no Dock icon).

    Standard keys always included:
        - CFBundleName, CFBundleDisplayName: App display name
        - CFBundleIdentifier: Unique bundle identifier
        - CFBundleVersion, CFBundleShortVersionString: Version strings
        - LSUIElement: True (no Dock icon)
        - NSHighResolutionCapable: True (Retina support)
        - LSMinimumSystemVersion: Minimum macOS version

    Args:
        name (str): Application display name (e.g., "My Awesome App").

        identifier (str): Bundle identifier in reverse-DNS format
            (e.g., "com.example.myapp").

        version (str): Version string (e.g., "1.0.0"). Used for both
            CFBundleVersion and CFBundleShortVersionString.

        min_macos (str): Minimum macOS version required (e.g., "13.0").

        plist_options (dict): Additional plist customizations. Supported keys:
            - ``copyright`` (str): NSHumanReadableCopyright value
            - ``category`` (str): LSApplicationCategoryType value
            - ``notification_style`` (str): NSUserNotificationAlertStyle
            - ``usage`` (dict): Privacy permission descriptions with keys:
                - ``microphone``: NSMicrophoneUsageDescription
                - ``camera``: NSCameraUsageDescription
                - ``location``: NSLocationUsageDescription
                - ``apple_events``: NSAppleEventsUsageDescription
            - ``url_schemes`` (list[str]): Custom URL schemes to register
            - ``custom`` (dict): Arbitrary additional plist keys

    Returns:
        dict: Complete Info.plist dictionary ready for serialization.

    Example:
        >>> plist = build_plist_dict(
        ...     name="My App",
        ...     identifier="com.example.myapp",
        ...     version="1.0.0",
        ...     min_macos="13.0",
        ...     plist_options={
        ...         "copyright": "Copyright 2024 Example Inc.",
        ...         "category": "public.app-category.utilities",
        ...         "url_schemes": ["myapp"],
        ...     }
        ... )
        >>> plist["CFBundleName"]
        'My App'
        >>> plist["LSUIElement"]
        True
    """
    plist = {
        "CFBundleName": name,
        "CFBundleDisplayName": name,
        "CFBundleIdentifier": identifier,
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "LSUIElement": True,
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": min_macos,
    }

    # Copyright
    if plist_options.get("copyright"):
        plist["NSHumanReadableCopyright"] = plist_options["copyright"]

    # App category
    if plist_options.get("category"):
        plist["LSApplicationCategoryType"] = plist_options["category"]

    # Notification style
    if plist_options.get("notification_style"):
        plist["NSUserNotificationAlertStyle"] = plist_options["notification_style"]

    # Usage descriptions (privacy permissions)
    usage = plist_options.get("usage", {})
    if usage.get("microphone"):
        plist["NSMicrophoneUsageDescription"] = usage["microphone"]
    if usage.get("camera"):
        plist["NSCameraUsageDescription"] = usage["camera"]
    if usage.get("location"):
        plist["NSLocationUsageDescription"] = usage["location"]
    if usage.get("apple_events"):
        plist["NSAppleEventsUsageDescription"] = usage["apple_events"]

    # URL schemes
    if plist_options.get("url_schemes"):
        plist["CFBundleURLTypes"] = [{
            "CFBundleURLName": identifier,
            "CFBundleURLSchemes": plist_options["url_schemes"],
        }]

    # Custom plist keys
    custom = plist_options.get("custom", {})
    plist.update(custom)

    return plist


def generate_setup_py(
    script: Path,
    name: str,
    packages: list[str],
    options: dict,
    plist_options: Optional[dict] = None,
) -> str:
    """Generate a setup.py file for py2app bundling.

    Creates a complete setup.py script configured for py2app that will bundle
    the Nib application. The generated script includes:

        - Proper package inclusion (nib, msgpack, user dependencies)
        - Optimized exclusion list (excludes unused installed packages)
        - Info.plist configuration
        - Icon file path (if provided)
        - Recursion limit increase (required for complex dependency graphs)

    Args:
        script (Path): Absolute path to the user's Python entry point script.
            This becomes the main executable in the app bundle.

        name (str): Application display name. Used in both the bundle
            configuration and as the setup() name parameter.

        packages (list[str]): List of third-party package names to include.
            These are added to the core packages (nib, msgpack) and py2app
            runtime dependencies.

        options (dict): Build options dictionary with keys:
            - ``identifier`` (str | None): Bundle identifier
            - ``version`` (str): Version string, defaults to "1.0.0"
            - ``icon`` (str): Path to ICNS icon file
            - ``min_macos`` (str | None): Minimum macOS version
            - ``excludes`` (list[str]): Additional packages to exclude

        plist_options (dict | None): Additional Info.plist customizations.
            Passed through to :func:`build_plist_dict`.

    Returns:
        str: Complete setup.py file contents as a string, ready to be
            written to disk and executed with py2app.

    Example:
        >>> setup_content = generate_setup_py(
        ...     script=Path("/app/main.py"),
        ...     name="My App",
        ...     packages=["requests", "numpy"],
        ...     options={"version": "2.0.0", "icon": "/tmp/app.icns"},
        ... )
        >>> print(setup_content[:50])
        \"\"\"Auto-generated setup.py for py2app.\"\"\"

    Note:
        The generated setup.py increases Python's recursion limit to handle
        complex dependency graphs that modulegraph may encounter.
    """
    identifier = options.get("identifier") or f"com.nib.{name.lower().replace(' ', '')}"
    version = options.get("version", "1.0.0")
    icon = options.get("icon", "")
    min_macos = options.get("min_macos") or get_macos_version()

    # Build plist dictionary
    plist = build_plist_dict(name, identifier, version, min_macos, plist_options or {})
    plist_str = repr(plist)

    # Build packages list
    # Include: nib, msgpack, user deps, and py2app runtime deps
    py2app_deps = ["altgraph", "macholib", "modulegraph", "packaging"]
    all_packages = ["nib", "msgpack"] + py2app_deps + packages
    packages_str = repr(all_packages)

    # pkg_resources needs these but we don't want all of setuptools
    pkg_resources_deps = ["pkg_resources", "jaraco.functools", "jaraco.text", "jaraco.context", "more_itertools", "platformdirs"]

    # Exclude ALL installed packages except what we explicitly need
    needed = set(p.lower().replace("-", "_") for p in all_packages)
    excludes = get_packages_to_exclude(needed)
    user_excludes = options.get("excludes", [])
    excludes = list(set(excludes + user_excludes))
    excludes_str = repr(excludes)

    return f'''"""Auto-generated setup.py for py2app."""
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 3)  # Increase for modulegraph

from setuptools import setup

APP = [{repr(str(script))}]
OPTIONS = {{
    "argv_emulation": False,
    "strip": True,
    "optimize": 2,
    "plist": {plist_str},
    "packages": {packages_str},
    "includes": {repr(pkg_resources_deps)},
    "excludes": {excludes_str},
    "iconfile": {repr(icon) if icon else "None"},
}}

setup(
    name={repr(name)},
    app=APP,
    options={{"py2app": OPTIONS}},
    setup_requires=["py2app"],
)
'''


def convert_icon_to_icns(icon_path: Path, output_dir: Path) -> Optional[Path]:
    """Convert an image file to macOS ICNS icon format.

    Converts PNG or other image formats to the ICNS format required for
    macOS app bundle icons. Uses native macOS tools (``sips`` and ``iconutil``)
    to ensure proper icon generation with all required sizes and resolutions.

    The conversion process:
        1. If input is already ICNS, simply copies to output directory
        2. Creates an iconset directory with all required sizes
        3. Uses ``sips`` to resize the source image for each size
        4. Generates both standard and @2x (Retina) variants
        5. Uses ``iconutil`` to compile the iconset into ICNS
        6. Cleans up temporary iconset directory

    Generated icon sizes: 16, 32, 64, 128, 256, 512, 1024 pixels
    (plus @2x variants up to 512x512)

    Args:
        icon_path (Path): Path to the source image file. Supports any format
            that macOS ``sips`` can read (PNG, JPEG, TIFF, etc.). For best
            results, provide a high-resolution PNG (1024x1024 or larger).

        output_dir (Path): Directory where the ICNS file will be written.
            Must exist and be writable.

    Returns:
        Path | None: Path to the generated ICNS file (``output_dir/AppIcon.icns``),
            or None if conversion failed. If input was already ICNS, returns
            the path to the copied file.

    Example:
        >>> from pathlib import Path
        >>> icns_path = convert_icon_to_icns(
        ...     Path("icon.png"),
        ...     Path("/tmp/build")
        ... )
        >>> if icns_path:
        ...     print(f"Icon created: {icns_path}")
        Icon created: /tmp/build/AppIcon.icns

    Note:
        This function requires macOS and uses the following native tools:
            - ``sips``: Scriptable Image Processing System
            - ``iconutil``: Icon conversion utility

        A warning is printed to stdout if conversion fails, but no exception
        is raised.
    """
    if icon_path.suffix.lower() == ".icns":
        # Already ICNS, just copy
        dest = output_dir / icon_path.name
        shutil.copy2(icon_path, dest)
        return dest

    # Create iconset directory
    iconset_dir = output_dir / "AppIcon.iconset"
    iconset_dir.mkdir(exist_ok=True)

    # Required sizes for macOS icons
    sizes = [16, 32, 64, 128, 256, 512, 1024]

    try:
        # Use sips to resize the image for each required size
        for size in sizes:
            # Regular resolution
            dest = iconset_dir / f"icon_{size}x{size}.png"
            subprocess.run(
                ["sips", "-z", str(size), str(size), str(icon_path), "--out", str(dest)],
                check=True,
                capture_output=True,
            )

            # Retina resolution (2x)
            if size <= 512:
                retina_size = size * 2
                dest_2x = iconset_dir / f"icon_{size}x{size}@2x.png"
                subprocess.run(
                    ["sips", "-z", str(retina_size), str(retina_size), str(icon_path), "--out", str(dest_2x)],
                    check=True,
                    capture_output=True,
                )

        # Convert iconset to icns
        icns_path = output_dir / "AppIcon.icns"
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(icns_path)],
            check=True,
            capture_output=True,
        )

        # Clean up iconset
        shutil.rmtree(iconset_dir)

        return icns_path

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to convert icon: {e}")
        return None


def build_app(
    script: Path,
    name: Optional[str] = None,
    output: Path = Path("dist"),
    icon: Optional[Path] = None,
    identifier: Optional[str] = None,
    version: str = "1.0.0",
    extra_deps: Optional[str] = None,
    min_macos: Optional[str] = None,
    excludes: Optional[str] = None,
    plist_options: Optional[dict] = None,
) -> int:
    """Build a standalone macOS .app bundle from a Nib script.

    This is the main build function that orchestrates the entire bundling
    process. It creates a self-contained macOS application that includes:

        - The Python interpreter and standard library
        - All detected third-party dependencies
        - The nib package and msgpack serialization library
        - The nib-runtime Swift executable
        - Application assets (icons, images, etc.)

    The resulting .app bundle can be distributed and run on any compatible
    macOS system without requiring Python or dependencies to be installed.

    Args:
        script (Path): Path to the Python entry point script. This script
            should contain a ``nib.run(main)`` call. The script is analyzed
            to detect dependencies and extract app metadata (title, icon).

        name (str | None): Application display name. If not provided, derived
            from either:
            1. ``app.title`` assignment in the script
            2. The script filename (titlecased, underscores to spaces)

        output (Path): Directory where the .app bundle will be created.
            Defaults to ``./dist/``. Created if it doesn't exist.

        icon (Path | None): Path to the application icon. Supports:
            - ``.icns``: Used directly
            - ``.png``: Converted to ICNS (1024x1024 recommended)
            If not provided, the app uses the default macOS app icon.

        identifier (str | None): Bundle identifier in reverse-DNS format
            (e.g., "com.company.appname"). Defaults to ``com.nib.<name>``.

        version (str): Application version string. Defaults to "1.0.0".
            Used in Info.plist for CFBundleVersion.

        extra_deps (str | None): Comma-separated list of additional pip
            package names to include beyond auto-detected dependencies.
            Useful when dynamic imports aren't detected automatically.

        min_macos (str | None): Minimum macOS version required to run the
            app (e.g., "13.0"). Defaults to the current macOS version.

        excludes (str | None): Comma-separated list of package names to
            exclude from bundling, even if detected as dependencies.

        plist_options (dict | None): Additional Info.plist customizations.
            See :func:`build_plist_dict` for supported options.

    Returns:
        int: Exit code indicating build result.
            - 0: Build completed successfully
            - 1: Build failed (script not found, runtime missing, py2app error)

    Example:
        Basic build::

            >>> exit_code = build_app(Path("src/main.py"))
            Using nib-runtime: /path/to/nib-runtime
            Building: Main
            Detecting dependencies...
            Running py2app...
            Success! App bundle created at: dist/Main.app
            >>> exit_code
            0

        Full configuration::

            >>> exit_code = build_app(
            ...     script=Path("src/main.py"),
            ...     name="My Awesome App",
            ...     output=Path("build/release"),
            ...     icon=Path("assets/icon.png"),
            ...     identifier="com.example.myawesomeapp",
            ...     version="2.1.0",
            ...     extra_deps="httpx,pillow",
            ...     min_macos="14.0",
            ...     plist_options={
            ...         "copyright": "Copyright 2024",
            ...         "category": "public.app-category.utilities",
            ...     },
            ... )

    Note:
        The nib-runtime Swift binary must be built before running this
        function. Build it with: ``cd swift && swift build -c release``

    See Also:
        - :func:`find_nib_runtime`: Locates the Swift runtime
        - :func:`convert_icon_to_icns`: Icon conversion
        - :func:`generate_setup_py`: py2app configuration generation
    """
    # Validate script exists
    script = script.resolve()
    if not script.exists():
        print(f"Error: Script not found: {script}")
        return 1

    # Find nib-runtime
    runtime = find_nib_runtime()
    if not runtime:
        print("Error: nib-runtime not found.")
        print("Please build it first: cd swift && swift build -c release")
        return 1

    print(f"Using nib-runtime: {runtime}")

    # Extract metadata from script
    metadata = extract_metadata(script)

    # Determine app name
    if not name:
        name = metadata.get("title") or script.stem.replace("_", " ").title()

    print(f"Building: {name}")

    # Detect dependencies
    print("Detecting dependencies...")
    imports = detect_imports(script)
    packages = resolve_packages(imports)

    # Add extra deps if provided
    if extra_deps:
        extra = [dep.strip() for dep in extra_deps.split(",") if dep.strip()]
        packages.extend(extra)

    if packages:
        print(f"  Dependencies: {', '.join(packages)}")
    else:
        print("  No third-party dependencies detected")

    # Create output directory
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    # Create temp build directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Handle icon
        icon_path = ""
        if icon:
            icon = icon.resolve()
            if icon.exists():
                icns = convert_icon_to_icns(icon, tmpdir)
                if icns:
                    icon_path = str(icns)
            else:
                print(f"Warning: Icon not found: {icon}")

        # Parse excludes
        exclude_list = []
        if excludes:
            exclude_list = [e.strip() for e in excludes.split(",") if e.strip()]

        # Generate setup.py
        setup_content = generate_setup_py(
            script,
            name,
            packages,
            {
                "identifier": identifier,
                "version": version,
                "icon": icon_path,
                "min_macos": min_macos,
                "excludes": exclude_list,
            },
            plist_options=plist_options,
        )

        setup_path = tmpdir / "setup.py"
        setup_path.write_text(setup_content)

        # Copy script to temp directory
        script_copy = tmpdir / script.name
        shutil.copy2(script, script_copy)

        # Run py2app
        print("Running py2app...")

        # Set up environment with path to nib package
        env = os.environ.copy()
        # nib package is at python/nib relative to project root
        nib_package_dir = Path(__file__).parent.parent.parent.resolve()
        pythonpath = str(nib_package_dir)
        if "PYTHONPATH" in env:
            pythonpath = f"{pythonpath}:{env['PYTHONPATH']}"
        env["PYTHONPATH"] = pythonpath

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(setup_path),
                    "py2app",
                    "--dist-dir",
                    str(output),
                ],
                cwd=tmpdir,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error: py2app failed")
            print(e.stdout)
            print(e.stderr)
            return 1

        # Inject nib-runtime into bundle
        app_path = output / f"{name}.app"
        if not app_path.exists():
            # Try with sanitized name
            for item in output.iterdir():
                if item.suffix == ".app":
                    app_path = item
                    break

        if not app_path.exists():
            print(f"Error: App bundle not created")
            return 1

        runtime_dst = app_path / "Contents" / "Resources" / "nib-runtime"
        shutil.copy2(runtime, runtime_dst)
        os.chmod(runtime_dst, 0o755)

        print(f"Bundled nib-runtime: {runtime_dst}")

        # Bundle assets directory
        assets_src = script.parent / "assets"
        if not assets_src.exists():
            # Try parent directory (for src/main.py -> src/assets structure)
            assets_src = script.parent.parent / "assets"
        if not assets_src.exists():
            # Try src/assets from script's parent
            assets_src = script.parent / "src" / "assets"

        if assets_src.exists() and assets_src.is_dir():
            assets_dst = app_path / "Contents" / "Resources" / "assets"
            shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)
            print(f"Bundled assets: {assets_dst}")

    print(f"\nSuccess! App bundle created at: {app_path}")
    print(f"Bundle size: {get_dir_size(app_path):.1f} MB")

    return 0


def get_dir_size(path: Path) -> float:
    """Calculate the total size of a directory in megabytes.

    Recursively sums the sizes of all files within the directory tree.
    Useful for reporting the final bundle size to the user.

    Args:
        path (Path): Path to the directory to measure.

    Returns:
        float: Total size in megabytes (MB). Symbolic links and
            directories themselves are not counted.

    Example:
        >>> size = get_dir_size(Path("dist/MyApp.app"))
        >>> print(f"Bundle size: {size:.1f} MB")
        Bundle size: 45.2 MB
    """
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
    return total / (1024 * 1024)
