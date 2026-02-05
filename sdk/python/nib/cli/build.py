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
        - https://github.com/astral-sh/python-build-standalone
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

from ..core.logging import logger
from .deps import detect_imports, extract_metadata, resolve_packages

# python-build-standalone configuration
PBS_VERSION = "20241219"
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
        logger.info(f"Using cached Python: {filename}")
        return cached_path

    logger.info(f"Downloading Python ({arch}): {filename}")

    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            last_logged_percent = -10  # Log every 10%
            with open(cached_path, "wb") as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = downloaded / total_size * 100
                        if progress - last_logged_percent >= 10:
                            logger.debug(f"Download progress: {progress:.0f}%")
                            last_logged_percent = progress
            logger.debug("Download complete")
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
    logger.info("Extracting Python distribution...")
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
    core_deps = ["msgpack"]  # used by nib so dep is mandatory
    all_packages = list(set(packages + core_deps))

    if not all_packages:
        logger.info("No dependencies to vendor")
    else:
        logger.info(f"Vendoring {len(all_packages)} packages...")
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
            logger.warn(f"pip install had issues: {result.stderr}")
            # don't fail - some packages might still have installed

    nib_src = Path(__file__).parent.parent.resolve()  # python/nib
    nib_dest = vendor_dir / "nib"
    if nib_dest.exists():
        shutil.rmtree(nib_dest)
    shutil.copytree(nib_src, nib_dest)

    logger.info(f"Vendored: {', '.join(all_packages)} + nib")


def cleanup_python_distribution(python_dir: Path) -> None:
    """Remove unnecessary files from Python distribution to reduce size.

    Args:
        python_dir: Path to the Python distribution directory.
    """
    remove_patterns = [
        "**/__pycache__",
        "**/test",
        "**/tests",
        "**/idle_test",
        "**/*.pyc",
        "**/*.pyo",
        "lib/python*/config-*",
        "lib/python*/lib-dynload/_test*.so",
        "share",
        "include",
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

    # Remove Tcl/Tk directories - they have versioned names that confuse codesign
    # (codesign treats *.*.* directories as bundles)
    lib_dir = python_dir / "lib"
    if lib_dir.exists():
        tcl_tk_patterns = [
            "tk*",
            "tcl*",
            "thread*",
            "itcl*",
            "tdbc*",
            "sqlite*",
        ]
        for pattern in tcl_tk_patterns:
            for path in lib_dir.glob(pattern):
                if path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except Exception:
                        pass

        # Also remove tkinter from lib-dynload
        for tk_so in lib_dir.glob("python*/lib-dynload/_tkinter*.so"):
            try:
                tk_so.unlink()
            except Exception:
                pass

    # Remove unnecessary executables from bin directory
    # We only need python3/python3.12 for runtime
    bin_dir = python_dir / "bin"
    if bin_dir.exists():
        keep_patterns = {"python3", "python3.12"}
        for item in bin_dir.iterdir():
            if item.is_file() and item.name not in keep_patterns:
                try:
                    item.unlink()
                except Exception:
                    pass

    # Remove pkgconfig directory (not needed at runtime, causes signing issues)
    pkgconfig_dir = lib_dir / "pkgconfig"
    if pkgconfig_dir.exists():
        try:
            shutil.rmtree(pkgconfig_dir)
        except Exception:
            pass


def compile_python_code(app_dir: Path) -> None:
    """Compile Python files to bytecode and remove source files.

    This provides basic code protection by converting .py files to .pyc
    (Python bytecode) and removing the original source files. Uses
    optimization level 2 which removes docstrings and assert statements.

    Args:
        app_dir: Path to the app directory containing Python files.
    """
    import compileall

    # Compile all .py files with optimization level 2
    # legacy=True puts .pyc next to .py instead of __pycache__
    compileall.compile_dir(
        str(app_dir),
        optimize=2,
        quiet=1,
        legacy=True,
    )

    # Remove all .py source files, keep .pyc
    for py_file in app_dir.rglob("*.py"):
        pyc_file = py_file.with_suffix(".pyc")
        if pyc_file.exists():
            py_file.unlink()


def obfuscate_python_code(app_dir: Path) -> bool:
    """Obfuscate Python bytecode files.

    Uses a custom obfuscator that modifies bytecode in-place without
    adding any wrapper code. This works with Python's module import system.

    Obfuscates:
    - co_filename: Source file path -> empty string
    - co_name: Function/class names -> empty string
    - co_firstlineno: Line number -> 1
    - co_linetable/co_lnotab: Line mapping -> empty bytes
    - co_varnames: Local variable names -> numbered (0, 1, 2...)

    Args:
        app_dir: Path to the app directory containing .pyc files.

    Returns:
        bool: True if obfuscation succeeded, False otherwise.
    """
    from .obfuscate import obfuscate_pyc

    pyc_files = list(app_dir.rglob("*.pyc"))

    if not pyc_files:
        logger.warn("No .pyc files to obfuscate")
        return True

    for pyc_file in pyc_files:
        try:
            obfuscate_pyc(pyc_file)
        except Exception as e:
            logger.warn(f"Failed to obfuscate {pyc_file.name}: {e}")
            return False

    logger.info(f"Obfuscated {len(pyc_files)} bytecode files")
    return True


def compile_python_native(app_dir: Path, python_dir: Path) -> bool:
    """Compile Python files to native .so modules using Cython.

    Converts .py files to C via Cython, then compiles to shared libraries
    with clang, optimized for size (-Os). Files that fail Cython compilation
    fall back to bytecode (.pyc).

    Args:
        app_dir: Path to the app directory containing Python files.
        python_dir: Path to the bundled python-build-standalone directory.

    Returns:
        bool: True if compilation succeeded (at least partially), False on fatal error.
    """
    try:
        from Cython.Compiler import Options as CythonGlobalOptions
        from Cython.Compiler.Main import compile as cython_compile
        from Cython.Compiler.Options import CompilationOptions
    except ImportError:
        logger.error(
            "Cython is required for --native. Install with: pip install cython"
        )
        return False

    import compileall
    import platform

    # Cython 3.x treats Python type hints as C type declarations by default,
    # which breaks code using Union types (e.g. Color where str is hinted).
    # Disable this via compiler directive.
    compiler_directives = {"annotation_typing": False}

    include_dir = python_dir / "include" / f"python{PYTHON_VERSION}"
    if not include_dir.exists():
        candidates = list((python_dir / "include").glob("python3.*"))
        if candidates:
            include_dir = candidates[0]
        else:
            logger.error(f"Python headers not found in {python_dir / 'include'}")
            return False

    python_bin = python_dir / "bin" / "python3"
    try:
        result = subprocess.run(
            [
                str(python_bin),
                "-c",
                "import importlib.machinery; print(importlib.machinery.EXTENSION_SUFFIXES[0])",
            ],
            capture_output=True,
            text=True,
            env={"PYTHONHOME": str(python_dir), "PATH": os.environ.get("PATH", "")},
        )
        so_suffix = result.stdout.strip()  # ".cpython-312-darwin.so"
    except Exception:
        so_suffix = f".cpython-{PYTHON_VERSION.replace('.', '')}-darwin.so"

    machine = platform.machine()
    arch = "arm64" if machine == "arm64" else "x86_64"
    arch_flags = ["-arch", arch]

    py_files = list(app_dir.rglob("*.py"))
    if not py_files:
        logger.warn("No .py files found to compile")
        return True

    # Handle main.py entry point: Swift runtime expects main.py or main.pyc,
    # so we rename it to _nib_app.py, compile that to .so, and create a tiny
    # main.py bootstrap that imports the compiled module.
    main_py = app_dir / "main.py"
    app_module = app_dir / "_nib_app.py"
    if main_py.exists():
        main_py.rename(app_module)
        py_files = [app_module if f == main_py else f for f in py_files]

    compiled = 0
    fell_back = 0
    total = len(py_files)

    for i, py_file in enumerate(py_files, 1):
        rel = py_file.relative_to(app_dir)
        c_file = py_file.with_suffix(".c")
        logger.progress(i, total, "Compiling")

        # 1 - cythonize .py → .c
        try:
            options = CompilationOptions(defaults=None)
            options.output_file = str(c_file)
            options.language_level = 3
            options.compiler_directives = compiler_directives
            result = cython_compile(str(py_file), options)
            if result.num_errors > 0:
                raise RuntimeError(f"Cython reported {result.num_errors} error(s)")
        except Exception as e:
            logger.debug(f"Cython failed for {rel}, falling back to .pyc: {e}")
            compileall.compile_file(str(py_file), optimize=2, quiet=1, legacy=True)
            pyc_file = py_file.with_suffix(".pyc")
            if pyc_file.exists():
                py_file.unlink()
            fell_back += 1
            continue

        if py_file.name == "__init__.py":
            so_file = py_file.parent / f"__init__{so_suffix}"
        else:
            so_file = py_file.with_suffix(so_suffix)

        # 2 - compile .c → .so (single step with clang)
        try:
            result = subprocess.run(
                [
                    "clang",
                    "-shared",
                    "-Os",
                    "-fPIC",
                    "-undefined",
                    "dynamic_lookup",
                    *arch_flags,
                    f"-I{include_dir}",
                    "-o",
                    str(so_file),
                    str(c_file),
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())
        except Exception as e:
            logger.debug(f"clang failed for {rel}, falling back to .pyc: {e}")
            c_file.unlink(missing_ok=True)
            compileall.compile_file(str(py_file), optimize=2, quiet=1, legacy=True)
            pyc_file = py_file.with_suffix(".pyc")
            if pyc_file.exists():
                py_file.unlink()
            fell_back += 1
            continue

        py_file.unlink()
        c_file.unlink()
        compiled += 1

    main_py.write_text("import _nib_app\n")

    logger.info(f"Native compiled {compiled} file(s), {fell_back} fell back to .pyc")
    return True


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
    # Note: Python is placed in Resources (not MacOS) to avoid code signing issues
    # with versioned directories like python3.12 that codesign treats as bundles
    contents = app_path / "Contents"
    macos = contents / "MacOS"
    resources = contents / "Resources"
    app_dir = resources / "app"
    vendor_dir = app_dir / "vendor"
    python_dir = resources / "python"

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
    2. Bundled binary in package (pip install)
    3. System PATH
    4. Common installation locations (~/.local/bin, /usr/local/bin, ~/.nib/bin)
    5. Relative to nib package (for editable pip installs during development)
    6. Relative to current working directory (for running from nib repo)

    Returns:
        Path | None: Path to the runtime if found.
    """
    # 1. Check environment variable first (highest priority)
    env_runtime = os.environ.get("NIB_RUNTIME")
    if env_runtime:
        path = Path(env_runtime)
        if path.exists() and path.is_file():
            return path

    # 2. Check bundled binary in package (installed via pip)
    bundled_runtime = Path(__file__).resolve().parent.parent / "bin" / "nib-runtime"
    if bundled_runtime.exists() and bundled_runtime.is_file():
        return bundled_runtime

    # 3. Check PATH (most portable)
    path_runtime = shutil.which("nib-runtime")
    if path_runtime:
        return Path(path_runtime)

    # 5. Check relative to nib package (editable install during development)
    # Walk up from nib/cli/build.py looking for package/.build directory
    try:
        current = Path(__file__).resolve().parent
        for _ in range(6):  # Don't go too far up
            package_build = current / "package" / ".build"
            if package_build.exists():
                for build_type in ["release", "debug"]:
                    runtime = package_build / build_type / "nib-runtime"
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


def detect_permission_usage(app_dir: Path) -> dict:
    """Scan Python source files for Permission.* usage and return required plist keys.

    Returns a dict mapping Info.plist key names to default usage description strings.
    Only Camera and Microphone require plist keys; Notifications does not.
    """
    import re

    pattern = re.compile(r"Permission\.(CAMERA|MICROPHONE)")
    plist_map = {
        "CAMERA": ("NSCameraUsageDescription", "This app requires camera access."),
        "MICROPHONE": (
            "NSMicrophoneUsageDescription",
            "This app requires microphone access.",
        ),
    }

    detected = {}
    for py_file in app_dir.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in pattern.finditer(content):
            perm = match.group(1)
            if perm in plist_map:
                key, desc = plist_map[perm]
                detected[key] = desc

    return detected


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
        "CFBundleExecutable": name,  # must match binary in MacOS/
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSUIElement": True,  # menu bar app - no Dock icon (maybe let user choose (?))
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": min_macos,
    }

    if fonts_path:
        plist["ATSApplicationFontsPath"] = fonts_path

    if plist_options.get("copyright"):
        plist["NSHumanReadableCopyright"] = plist_options["copyright"]

    if plist_options.get("category"):
        plist["LSApplicationCategoryType"] = plist_options["category"]

    if plist_options.get("notification_style"):
        plist["NSUserNotificationAlertStyle"] = plist_options["notification_style"]

    usage = plist_options.get("usage", {})
    if usage.get("microphone"):
        plist["NSMicrophoneUsageDescription"] = usage["microphone"]
    if usage.get("camera"):
        plist["NSCameraUsageDescription"] = usage["camera"]
    if usage.get("location"):
        plist["NSLocationUsageDescription"] = usage["location"]
    if usage.get("apple_events"):
        plist["NSAppleEventsUsageDescription"] = usage["apple_events"]

    if plist_options.get("url_schemes"):
        plist["CFBundleURLTypes"] = [
            {
                "CFBundleURLName": identifier,
                "CFBundleURLSchemes": plist_options["url_schemes"],
            }
        ]

    custom = plist_options.get("custom", {})
    plist.update(custom)

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
        logger.warn(f"Failed to convert icon: {e}")
        return None


def codesign_app(app_path: Path) -> bool:
    """Sign the app bundle with ad-hoc signature.

    This is required for features like SMAppService (launch at login) to work.
    The app is signed with ad-hoc signature (no Developer ID required).

    Note: Due to versioned directories in the Python distribution (e.g., python3.12),
    full bundle signing may fail. We sign the main executable which is what matters
    for most features.

    Args:
        app_path: Path to the .app bundle.

    Returns:
        bool: True if signing succeeded.
    """
    try:
        # Sign all .dylib files first
        for dylib in app_path.rglob("*.dylib"):
            subprocess.run(
                ["codesign", "--force", "--sign", "-", str(dylib)],
                capture_output=True,
                check=False,
            )

        # Sign all .so files
        for so_file in app_path.rglob("*.so"):
            subprocess.run(
                ["codesign", "--force", "--sign", "-", str(so_file)],
                capture_output=True,
                check=False,
            )

        # Sign all executables in Python bin directory (Python is in Resources)
        python_bin_dir = app_path / "Contents" / "Resources" / "python" / "bin"
        if python_bin_dir.exists():
            for item in python_bin_dir.iterdir():
                if item.is_file():
                    # Check if it's a Mach-O executable
                    result = subprocess.run(
                        ["file", str(item)],
                        capture_output=True,
                        text=True,
                    )
                    if "Mach-O" in result.stdout:
                        subprocess.run(
                            ["codesign", "--force", "--sign", "-", str(item)],
                            capture_output=True,
                            check=False,
                        )

        # Get the app name from the bundle
        app_name = app_path.stem  # "My App" from "My App.app"
        main_executable = app_path / "Contents" / "MacOS" / app_name

        # Sign the main executable with runtime option for notarization compatibility
        main_signed = False
        if main_executable.exists():
            result = subprocess.run(
                [
                    "codesign",
                    "--force",
                    "--options",
                    "runtime",
                    "--sign",
                    "-",
                    str(main_executable),
                ],
                capture_output=True,
                check=False,
            )
            main_signed = result.returncode == 0

        # Try to sign the app bundle (may fail due to versioned directories)
        # This isn't strictly required if the main executable is signed
        subprocess.run(
            ["codesign", "--force", "--sign", "-", str(app_path)],
            capture_output=True,
            check=False,
        )

        # Return success if at least the main executable is signed
        return main_signed
    except Exception:
        return False


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
    no_compile: bool = False,
    obfuscate: bool = False,
    native: bool = False,
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
        launch_at_login: Enable launch at login (default: False).
        no_compile: Skip bytecode compilation, keep source files (default: False).
        obfuscate: Apply real obfuscation via pyc-zipper (default: False).

    Returns:
        int: Exit code (0 = success, 1 = failure).
    """
    script = script.resolve()
    if not script.exists():
        logger.error(f"Script not found: {script}")
        return 1

    runtime = find_nib_runtime()
    if not runtime:
        logger.error("nib-runtime not found.")
        logger.error("Please build it first: make build-runtime")
        logger.error("Or manually: cd package && swift build -c release")
        return 1

    logger.info(f"Using nib-runtime: {runtime}")

    metadata = extract_metadata(script)

    if not name:
        name = metadata.get("title") or script.stem.replace("_", " ").title()

    logger.info(f"Building: {name}")

    if arch is None:
        arch = platform.machine()
        if arch == "arm64":
            pass
        elif arch in ("x86_64", "AMD64"):
            arch = "x86_64"
        else:
            logger.warn(f"Unknown architecture {arch}, defaulting to arm64")
            arch = "arm64"

    logger.info(f"Target architecture: {arch}")

    if explicit_deps:
        logger.info("Using dependencies from pyproject.toml...")
        packages = list(explicit_deps)
    else:
        logger.info("Detecting dependencies...")
        project_dir = script.parent
        if project_dir.name == "src":
            project_dir = project_dir.parent
        imports = detect_imports(script, project_dir)
        packages = resolve_packages(imports)

    if extra_deps:
        extra = [dep.strip() for dep in extra_deps.split(",") if dep.strip()]
        packages.extend(extra)

    if packages:
        logger.info(f"Dependencies: {', '.join(packages)}")
    else:
        logger.info("No third-party dependencies")

    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    logger.info("Creating bundle structure...")
    paths = create_bundle_structure(output, name)

    logger.info("Setting up Python runtime...")
    try:
        python_archive = download_python_standalone(arch)
    except RuntimeError as e:
        logger.error(str(e))
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        python_extracted = extract_python_standalone(python_archive, tmpdir)

        # Move to final location
        if paths["python_dir"].exists():
            shutil.rmtree(paths["python_dir"])
        shutil.move(str(python_extracted), str(paths["python_dir"]))

    python_bin = paths["python_dir"] / "bin" / "python3"

    logger.info("Installing dependencies...")
    vendor_dependencies(python_bin, paths["vendor_dir"], packages)

    logger.info("Copying application code...")  # user code
    main_dest = paths["app_dir"] / "main.py"
    shutil.copy2(script, main_dest)

    script_dir = script.parent
    for item in script_dir.iterdir():
        if item == script:
            continue
        if item.name.startswith((".", "__")):
            continue
        if item.name == "assets":
            continue
        if item.is_file() and item.suffix == ".py":
            shutil.copy2(item, paths["app_dir"] / item.name)
        elif item.is_dir():
            is_package = (item / "__init__.py").exists()
            has_py_files = any(item.glob("*.py"))
            if is_package or has_py_files:
                dest = paths["app_dir"] / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(
                    item, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
                )

    assets_src = None
    for assets_path in [
        script_dir / "assets",
        script_dir.parent / "assets",
        script_dir / "src" / "assets",
    ]:
        if assets_path.exists() and assets_path.is_dir():
            assets_src = assets_path
            break

    # fonts path for Info.plist registration
    fonts_plist_path = None

    if assets_src:
        assets_dest = paths["resources"] / "assets"
        shutil.copytree(assets_src, assets_dest, dirs_exist_ok=True)
        logger.info(f"Copied assets from {assets_src}")

        fonts = detect_fonts_in_assets(assets_dest)
        if fonts:
            font_dirs = set()
            for font in fonts:
                font_path = Path(font)
                if font_path.parent != Path("."):
                    font_dirs.add(str(font_path.parent))

            if font_dirs and len(font_dirs) == 1 and "fonts" in list(font_dirs)[0]:
                fonts_plist_path = f"assets/{list(font_dirs)[0]}"
            else:
                fonts_plist_path = "assets"

            logger.info(f"Registered {len(fonts)} font(s) in {fonts_plist_path}")

    # Auto-detect permission usage before compilation removes .py files
    detected_permissions = detect_permission_usage(paths["app_dir"])

    # compile (native .so, bytecode .pyc, or keep source)
    if not no_compile:
        if native:
            logger.info("Compiling Python to native code with Cython...")
            if not compile_python_native(paths["app_dir"], paths["python_dir"]):
                logger.warn("Native compilation failed, falling back to bytecode")
                compile_python_code(paths["app_dir"])
        else:
            logger.info("Compiling Python bytecode...")
            compile_python_code(paths["app_dir"])

            if obfuscate:
                logger.info("Obfuscating Python bytecode...")
                if not obfuscate_python_code(paths["app_dir"]):
                    logger.warn("Obfuscation failed, continuing with compiled bytecode")

    logger.info("Installing Swift runtime...")
    swift_dest = paths["macos"] / name
    shutil.copy2(runtime, swift_dest)
    os.chmod(swift_dest, 0o755)

    icon_filename = None
    if icon:
        icon = icon.resolve()
        if icon.exists():
            icns = convert_icon_to_icns(icon, paths["resources"])
            if icns:
                icon_filename = icns.name
        else:
            logger.warn(f"Icon not found: {icon}")

    logger.info("Generating Info.plist...")
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

    # Inject auto-detected permission plist keys
    for plist_key, default_desc in detected_permissions.items():
        if plist_key not in plist:
            plist[plist_key] = default_desc
            logger.info(f"Auto-detected permission: {plist_key}")

    plist_path = paths["contents"] / "Info.plist"
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    # Clean up Python distribution to reduce size
    logger.info("Cleaning up...")
    cleanup_python_distribution(paths["python_dir"])

    # Also clean vendor directory
    for pycache in paths["vendor_dir"].rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)

    # Code sign the app bundle (required for SMAppService/launch at login)
    logger.info("Signing app bundle...")
    if codesign_app(paths["app"]):
        logger.info("App signed with ad-hoc signature")
    else:
        logger.warn("Code signing failed (some features may not work)")

    logger.success(f"App bundle created at: {paths['app']}")
    logger.success(f"Bundle size: {get_dir_size(paths['app']):.1f} MB")

    return 0
