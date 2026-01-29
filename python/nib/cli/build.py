"""Build standalone macOS app bundles from Nib scripts.

This module provides functionality to bundle Nib applications as standalone
macOS ``.app`` bundles using python-build-standalone. It handles the complete
build pipeline:

    - Download and embed a portable Python distribution
    - Vendor dependencies using pip install --target
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
    4. Create the .app bundle directory structure
    5. Download and extract python-build-standalone
    6. Vendor dependencies with pip install --target
    7. Copy user code and assets
    8. Install Swift runtime as main executable
    9. Generate Info.plist

Example:
    Building from command line::

        $ nib build myapp.py --name "My App" --icon icon.png
        Using nib-runtime: /path/to/nib-runtime
        Building: My App
        Target architecture: arm64
        Detecting dependencies...
          Dependencies: requests, numpy
        Setting up Python runtime...
        Installing dependencies...
        Success! App bundle created at: dist/My App.app
        Bundle size: 65.2 MB

Configuration via pyproject.toml:
    The build command integrates with ``[tool.nib.build]`` settings::

        [tool.nib.build]
        name = "My App"
        identifier = "com.example.myapp"
        version = "1.0.0"
        icon = "src/assets/icon.png"
        min_macos = "13.0"

Requirements:
    - macOS (uses native tools: sips, iconutil)
    - nib-runtime Swift binary built
    - Internet connection (for downloading Python)
"""

import os
import platform
import plistlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Literal, Optional

from .deps import detect_imports, extract_metadata, resolve_packages

# python-build-standalone configuration
PBS_VERSION = "20241219"  # Pin to a known good release
PYTHON_VERSION = "3.12"


def get_cache_dir() -> Path:
    """Get the cache directory for downloaded artifacts.

    Returns:
        Path: Cache directory path (created if it doesn't exist).
    """
    cache_dir = Path.home() / ".cache" / "nib"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_python_standalone_url(arch: Literal["arm64", "x86_64"]) -> str:
    """Get download URL for python-build-standalone distribution.

    Args:
        arch: Target architecture ("arm64" or "x86_64").

    Returns:
        str: Full download URL for the distribution.
    """
    arch_map = {
        "arm64": "aarch64",
        "x86_64": "x86_64",
    }
    pbs_arch = arch_map[arch]
    # Use install_only variant - smaller, sufficient for runtime
    filename = f"cpython-{PYTHON_VERSION}.8+{PBS_VERSION}-{pbs_arch}-apple-darwin-install_only.tar.gz"
    return f"https://github.com/astral-sh/python-build-standalone/releases/download/{PBS_VERSION}/{filename}"


def download_python_standalone(arch: str) -> Path:
    """Download python-build-standalone distribution, using cache if available.

    Args:
        arch: Target architecture ("arm64" or "x86_64").

    Returns:
        Path: Path to the downloaded archive file.

    Raises:
        RuntimeError: If download fails.
    """
    cache_dir = get_cache_dir()
    url = get_python_standalone_url(arch)
    filename = url.split("/")[-1]
    cached_path = cache_dir / filename

    if cached_path.exists():
        print(f"  Using cached Python: {filename}")
        return cached_path

    print(f"  Downloading Python ({arch}): {filename}")

    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            with open(cached_path, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = downloaded / total_size * 100
                        print(f"\r  Progress: {progress:.1f}%", end="", flush=True)
            print()  # Newline after progress
    except Exception as e:
        if cached_path.exists():
            cached_path.unlink()
        raise RuntimeError(f"Failed to download Python: {e}")

    return cached_path


def extract_python_standalone(archive_path: Path, dest_dir: Path) -> Path:
    """Extract python-build-standalone archive to destination.

    Args:
        archive_path: Path to the .tar.gz archive.
        dest_dir: Directory to extract to.

    Returns:
        Path: Path to the extracted Python directory.
    """
    print("  Extracting Python distribution...")
    with tarfile.open(archive_path, "r:gz") as tar:
        tar.extractall(dest_dir)

    # The archive extracts to a 'python' subdirectory
    python_dir = dest_dir / "python"
    if not python_dir.exists():
        # Some versions may extract differently
        for item in dest_dir.iterdir():
            if item.is_dir() and item.name.startswith("python"):
                python_dir = item
                break

    return python_dir


def vendor_dependencies(
    python_bin: Path,
    vendor_dir: Path,
    packages: list[str],
) -> None:
    """Install dependencies using pip --target.

    Args:
        python_bin: Path to the Python executable.
        vendor_dir: Directory to install packages to.
        packages: List of package names to install.
    """
    # Always include nib's core dependencies
    core_deps = ["msgpack"]
    all_packages = list(set(packages + core_deps))

    if not all_packages:
        print("  No dependencies to vendor")
    else:
        print(f"  Vendoring {len(all_packages)} packages...")
        vendor_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            str(python_bin),
            "-m",
            "pip",
            "install",
            "--target",
            str(vendor_dir),
            "--no-user",
            "--no-compile",
            "--disable-pip-version-check",
            "--quiet",
        ] + all_packages

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Warning: pip install had issues: {result.stderr}")
            # Don't fail - some packages might still have installed

    # Copy nib package to vendor
    nib_src = Path(__file__).parent.parent.resolve()  # python/nib
    nib_dest = vendor_dir / "nib"
    if nib_dest.exists():
        shutil.rmtree(nib_dest)
    shutil.copytree(nib_src, nib_dest)

    print(f"  Vendored: {', '.join(all_packages)} + nib")


def cleanup_python_distribution(python_dir: Path) -> None:
    """Remove unnecessary files from Python distribution to reduce size.

    Args:
        python_dir: Path to the Python distribution directory.
    """
    # Patterns to remove
    remove_patterns = [
        "**/__pycache__",
        "**/test",
        "**/tests",
        "**/idle_test",
        "**/*.pyc",
        "**/*.pyo",
        "lib/python*/config-*",
        "lib/python*/lib-dynload/_test*.so",
        "share",  # Documentation
        "include",  # Headers (not needed for runtime)
    ]

    for pattern in remove_patterns:
        for path in python_dir.glob(pattern):
            if path.exists():
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                except Exception:
                    pass  # Ignore errors during cleanup


def create_bundle_structure(output_dir: Path, name: str) -> dict[str, Path]:
    """Create the .app bundle directory structure.

    Args:
        output_dir: Directory to create the bundle in.
        name: Application name.

    Returns:
        dict: Dictionary mapping role names to paths.
    """
    app_path = output_dir / f"{name}.app"

    # Remove existing bundle
    if app_path.exists():
        shutil.rmtree(app_path)

    # Create structure
    contents = app_path / "Contents"
    macos = contents / "MacOS"
    resources = contents / "Resources"
    app_dir = resources / "app"
    vendor_dir = app_dir / "vendor"
    python_dir = macos / "python"

    for d in [macos, resources, app_dir, vendor_dir, python_dir]:
        d.mkdir(parents=True, exist_ok=True)

    return {
        "app": app_path,
        "contents": contents,
        "macos": macos,
        "resources": resources,
        "app_dir": app_dir,
        "vendor_dir": vendor_dir,
        "python_dir": python_dir,
    }


def find_nib_runtime() -> Optional[Path]:
    """Find the nib-runtime Swift executable.

    Searches in the following order:
    1. NIB_RUNTIME environment variable
    2. System PATH
    3. Common installation locations (~/.local/bin, /usr/local/bin, ~/.nib/bin)
    4. Relative to nib package (for editable pip installs during development)
    5. Relative to current working directory (for running from nib repo)

    Returns:
        Path | None: Path to the runtime if found.
    """
    # 1. Check environment variable first (highest priority)
    env_runtime = os.environ.get("NIB_RUNTIME")
    if env_runtime:
        path = Path(env_runtime)
        if path.exists() and path.is_file():
            return path

    # 2. Check PATH (most portable)
    path_runtime = shutil.which("nib-runtime")
    if path_runtime:
        return Path(path_runtime)

    # 4. Check relative to nib package (editable install during development)
    # Walk up from nib/cli/build.py looking for swift/.build directory
    try:
        current = Path(__file__).resolve().parent
        for _ in range(6):  # Don't go too far up
            swift_build = current / "swift" / ".build"
            if swift_build.exists():
                for build_type in ["release", "debug"]:
                    runtime = swift_build / build_type / "nib-runtime"
                    if runtime.exists() and runtime.is_file():
                        return runtime
            current = current.parent
    except Exception:
        pass

    return None


def get_macos_version() -> str:
    """Get the current macOS version for LSMinimumSystemVersion.

    Returns:
        str: macOS version string (e.g., "14.0").
    """
    version = platform.mac_ver()[0]
    if version:
        parts = version.split(".")
        if len(parts) >= 2:
            return f"{parts[0]}.0"
    return "13.0"


def detect_fonts_in_assets(assets_dir: Path) -> list[str]:
    """Detect font files in the assets directory.

    Args:
        assets_dir: Path to the assets directory.

    Returns:
        list[str]: List of relative paths to font files from assets directory.
    """
    font_extensions = {".ttf", ".otf", ".ttc", ".woff", ".woff2"}
    fonts = []

    if not assets_dir.exists():
        return fonts

    for font_file in assets_dir.rglob("*"):
        if font_file.is_file() and font_file.suffix.lower() in font_extensions:
            # Get relative path from assets directory
            rel_path = font_file.relative_to(assets_dir)
            fonts.append(str(rel_path))

    return fonts


def build_plist_dict(
    name: str,
    identifier: str,
    version: str,
    min_macos: str,
    plist_options: dict,
    fonts_path: Optional[str] = None,
    launch_at_login: bool = False,
) -> dict:
    """Build the Info.plist dictionary for the macOS app bundle.

    Args:
        name: Application display name.
        identifier: Bundle identifier.
        version: Version string.
        min_macos: Minimum macOS version.
        plist_options: Additional plist options.
        fonts_path: Relative path to fonts directory from Resources (e.g., "assets/fonts").

    Returns:
        dict: Complete Info.plist dictionary.
    """
    plist = {
        "CFBundleName": name,
        "CFBundleDisplayName": name,
        "CFBundleIdentifier": identifier,
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "CFBundleExecutable": name,  # Must match binary in MacOS/
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSUIElement": True,  # Menu bar app - no Dock icon
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": min_macos,
    }

    # Register fonts directory if fonts are present
    if fonts_path:
        plist["ATSApplicationFontsPath"] = fonts_path

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
        plist["CFBundleURLTypes"] = [
            {
                "CFBundleURLName": identifier,
                "CFBundleURLSchemes": plist_options["url_schemes"],
            }
        ]

    # Custom plist keys
    custom = plist_options.get("custom", {})
    plist.update(custom)

    # Launch at login
    if launch_at_login:
        plist["NibLaunchAtLogin"] = True

    return plist


def convert_icon_to_icns(icon_path: Path, output_dir: Path) -> Optional[Path]:
    """Convert an image file to macOS ICNS icon format.

    Args:
        icon_path: Path to the source image.
        output_dir: Directory to write the ICNS file.

    Returns:
        Path | None: Path to the ICNS file, or None if conversion failed.
    """
    if icon_path.suffix.lower() == ".icns":
        dest = output_dir / icon_path.name
        shutil.copy2(icon_path, dest)
        return dest

    # Create iconset directory
    iconset_dir = output_dir / "AppIcon.iconset"
    iconset_dir.mkdir(exist_ok=True)

    sizes = [16, 32, 64, 128, 256, 512, 1024]

    try:
        for size in sizes:
            dest = iconset_dir / f"icon_{size}x{size}.png"
            subprocess.run(
                [
                    "sips",
                    "-z",
                    str(size),
                    str(size),
                    str(icon_path),
                    "--out",
                    str(dest),
                ],
                check=True,
                capture_output=True,
            )

            if size <= 512:
                retina_size = size * 2
                dest_2x = iconset_dir / f"icon_{size}x{size}@2x.png"
                subprocess.run(
                    [
                        "sips",
                        "-z",
                        str(retina_size),
                        str(retina_size),
                        str(icon_path),
                        "--out",
                        str(dest_2x),
                    ],
                    check=True,
                    capture_output=True,
                )

        icns_path = output_dir / "AppIcon.icns"
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir), "-o", str(icns_path)],
            check=True,
            capture_output=True,
        )

        shutil.rmtree(iconset_dir)
        return icns_path

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to convert icon: {e}")
        return None


def get_dir_size(path: Path) -> float:
    """Calculate total directory size in megabytes.

    Args:
        path: Directory path.

    Returns:
        float: Size in MB.
    """
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
    return total / (1024 * 1024)


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
    explicit_deps: Optional[list[str]] = None,
    arch: Optional[str] = None,
    launch_at_login: bool = False,
) -> int:
    """Build a standalone macOS .app bundle from a Nib script.

    This function creates a self-contained macOS application using
    python-build-standalone for the Python runtime.

    Args:
        script: Path to the Python entry point script.
        name: Application display name (default: from script metadata).
        output: Output directory (default: ./dist/).
        icon: Path to application icon (.png or .icns).
        identifier: Bundle identifier (default: com.nib.<name>).
        version: Application version (default: "1.0.0").
        extra_deps: Comma-separated additional dependencies.
        min_macos: Minimum macOS version (default: current version).
        excludes: Comma-separated packages to exclude (unused in standalone mode).
        plist_options: Additional Info.plist customizations.
        explicit_deps: Explicit dependency list (from pyproject.toml).
        arch: Target architecture ("arm64" or "x86_64", default: current).

    Returns:
        int: Exit code (0 = success, 1 = failure).
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

    # Determine target architecture
    if arch is None:
        arch = platform.machine()
        if arch == "arm64":
            pass
        elif arch in ("x86_64", "AMD64"):
            arch = "x86_64"
        else:
            print(f"Warning: Unknown architecture {arch}, defaulting to arm64")
            arch = "arm64"

    print(f"Target architecture: {arch}")

    # Determine dependencies
    if explicit_deps:
        print("Using dependencies from pyproject.toml...")
        packages = list(explicit_deps)
    else:
        print("Detecting dependencies...")
        project_dir = script.parent
        if project_dir.name == "src":
            project_dir = project_dir.parent
        imports = detect_imports(script, project_dir)
        packages = resolve_packages(imports)

    # Add extra deps if provided
    if extra_deps:
        extra = [dep.strip() for dep in extra_deps.split(",") if dep.strip()]
        packages.extend(extra)

    if packages:
        print(f"  Dependencies: {', '.join(packages)}")
    else:
        print("  No third-party dependencies")

    # Create output directory
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    # Create bundle structure
    print("Creating bundle structure...")
    paths = create_bundle_structure(output, name)

    # Download and extract Python
    print("Setting up Python runtime...")
    try:
        python_archive = download_python_standalone(arch)
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1

    # Extract to a temp location first, then move
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        python_extracted = extract_python_standalone(python_archive, tmpdir)

        # Move to final location
        if paths["python_dir"].exists():
            shutil.rmtree(paths["python_dir"])
        shutil.move(str(python_extracted), str(paths["python_dir"]))

    python_bin = paths["python_dir"] / "bin" / "python3"

    # Vendor dependencies
    print("Installing dependencies...")
    vendor_dependencies(python_bin, paths["vendor_dir"], packages)

    # Copy user code
    print("Copying application code...")
    main_dest = paths["app_dir"] / "main.py"
    shutil.copy2(script, main_dest)

    # Copy any sibling Python files and packages
    script_dir = script.parent
    for item in script_dir.iterdir():
        if item == script:
            continue
        if item.name.startswith((".", "__")):
            continue
        if item.name == "assets":
            continue  # Assets are handled separately
        if item.is_file() and item.suffix == ".py":
            shutil.copy2(item, paths["app_dir"] / item.name)
        elif item.is_dir():
            # Copy if it's a package (__init__.py) or contains any Python files
            is_package = (item / "__init__.py").exists()
            has_py_files = any(item.glob("*.py"))
            if is_package or has_py_files:
                dest = paths["app_dir"] / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(
                    item, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
                )

    # Copy assets
    assets_src = None
    for assets_path in [
        script_dir / "assets",
        script_dir.parent / "assets",
        script_dir / "src" / "assets",
    ]:
        if assets_path.exists() and assets_path.is_dir():
            assets_src = assets_path
            break

    # Track fonts path for Info.plist registration
    fonts_plist_path = None

    if assets_src:
        assets_dest = paths["resources"] / "assets"
        shutil.copytree(assets_src, assets_dest, dirs_exist_ok=True)
        print(f"  Copied assets from {assets_src}")

        # Detect fonts in assets for Info.plist registration
        fonts = detect_fonts_in_assets(assets_dest)
        if fonts:
            # Find the common font directory
            # If all fonts are in assets/fonts/, use "assets/fonts"
            # Otherwise use "assets" as the base
            font_dirs = set()
            for font in fonts:
                font_path = Path(font)
                if font_path.parent != Path("."):
                    font_dirs.add(str(font_path.parent))

            if font_dirs and len(font_dirs) == 1 and "fonts" in list(font_dirs)[0]:
                fonts_plist_path = f"assets/{list(font_dirs)[0]}"
            else:
                fonts_plist_path = "assets"

            print(f"  Registered {len(fonts)} font(s) in {fonts_plist_path}")

    # Copy Swift runtime as main executable
    print("Installing Swift runtime...")
    swift_dest = paths["macos"] / name
    shutil.copy2(runtime, swift_dest)
    os.chmod(swift_dest, 0o755)

    # Handle icon
    icon_filename = None
    if icon:
        icon = icon.resolve()
        if icon.exists():
            icns = convert_icon_to_icns(icon, paths["resources"])
            if icns:
                icon_filename = icns.name
        else:
            print(f"Warning: Icon not found: {icon}")

    # Generate Info.plist
    print("Generating Info.plist...")
    plist = build_plist_dict(
        name=name,
        identifier=identifier or f"com.nib.{name.lower().replace(' ', '')}",
        version=version,
        min_macos=min_macos or get_macos_version(),
        plist_options=plist_options or {},
        fonts_path=fonts_plist_path,
        launch_at_login=launch_at_login,
    )

    if icon_filename:
        plist["CFBundleIconFile"] = icon_filename

    plist_path = paths["contents"] / "Info.plist"
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    # Clean up Python distribution to reduce size
    print("Cleaning up...")
    cleanup_python_distribution(paths["python_dir"])

    # Also clean vendor directory
    for pycache in paths["vendor_dir"].rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)

    print(f"\nSuccess! App bundle created at: {paths['app']}")
    print(f"Bundle size: {get_dir_size(paths['app']):.1f} MB")

    return 0
