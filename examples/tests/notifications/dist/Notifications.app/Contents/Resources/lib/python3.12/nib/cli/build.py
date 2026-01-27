"""Build standalone macOS app bundles from nib scripts."""

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
    """Find the nib-runtime executable.

    Returns:
        Path to nib-runtime, or None if not found.
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
    """Get all installed third-party packages."""
    try:
        from importlib.metadata import distributions
        return {dist.metadata["Name"].lower().replace("-", "_") for dist in distributions()}
    except ImportError:
        return set()


def get_packages_to_exclude(needed: set[str]) -> list[str]:
    """Get list of installed packages to exclude (everything except needed).

    Args:
        needed: Set of package names that should be included.

    Returns:
        List of package names to exclude.
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
    """Get the current macOS version for LSMinimumSystemVersion."""
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
    """Build the Info.plist dictionary.

    Args:
        name: App name.
        identifier: Bundle identifier.
        version: App version.
        min_macos: Minimum macOS version.
        plist_options: Additional plist options from config.

    Returns:
        Dictionary of plist entries.
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
    """Generate a setup.py file for py2app.

    Args:
        script: Path to the user's Python script.
        name: App name.
        packages: List of packages to include.
        options: Additional options (identifier, version, icon).
        plist_options: Additional plist options from config.

    Returns:
        Contents of setup.py as a string.
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
    """Convert a PNG or other image to ICNS format.

    Uses macOS iconutil command.

    Args:
        icon_path: Path to the source image.
        output_dir: Directory to write the ICNS file.

    Returns:
        Path to the ICNS file, or None if conversion failed.
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
    """Build a standalone macOS .app bundle from a nib script.

    Args:
        script: Path to the Python script.
        name: App name (default: derived from script).
        output: Output directory for the .app bundle.
        icon: Path to icon file (.icns or .png).
        identifier: Bundle identifier.
        version: App version string.
        extra_deps: Comma-separated list of additional pip packages.
        min_macos: Minimum macOS version (default: current).
        excludes: Comma-separated list of packages to exclude.
        plist_options: Additional Info.plist options.

    Returns:
        Exit code (0 for success).
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
    """Get the size of a directory in MB."""
    total = 0
    for item in path.rglob("*"):
        if item.is_file():
            total += item.stat().st_size
    return total / (1024 * 1024)
