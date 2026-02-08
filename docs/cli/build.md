# nib build

Build a standalone macOS `.app` bundle from a Nib application. The output is a self-contained application that runs without requiring Python or any dependencies on the target system.

## Usage

```bash
nib build [script.py] [options]
```

If no script is specified, `nib build` reads the entry point from `pyproject.toml`:

```bash
nib build                # Uses [tool.nib] entry (defaults to src/main.py)
nib build src/main.py    # Explicit script path
```

The resulting bundle is written to `dist/AppName.app` by default.

## Options

### General

| Flag | Description |
|------|-------------|
| `-o`, `--output <dir>` | Output directory (default: `dist/`) |
| `-n`, `--name <name>` | App display name (default: from pyproject.toml or script name) |
| `-i`, `--icon <path>` | Icon file -- `.icns` or `.png` (PNG is auto-converted to ICNS) |
| `--identifier <id>` | Bundle identifier (default: `com.nib.<name>`) |
| `--version <ver>` | App version string (default: `1.0.0`) |
| `--extra-deps <pkgs>` | Additional pip packages to include, comma-separated |
| `--exclude <pkgs>` | Packages to exclude from bundling, comma-separated |
| `--min-macos <ver>` | Minimum macOS version (default: current system version) |
| `--arch <arch>` | Target architecture: `arm64` or `x86_64` (default: current machine) |
| `-v`, `--verbose` | Verbose build output |

### Code protection

| Flag | Description |
|------|-------------|
| `--native` | Compile `.py` files to native `.so` modules via Cython |
| `--obfuscate` | Strip debug info from `.pyc` bytecode (function names, line numbers, variable names) |
| `--no-compile` | Keep `.py` source files as-is (skip bytecode compilation) |

By default, Python files are compiled to `.pyc` bytecode with optimization level 2 (docstrings and asserts removed).

!!! warning "Mutually exclusive flags"
    - `--native` and `--no-compile` cannot be used together
    - `--obfuscate` and `--no-compile` cannot be used together
    - `--native` and `--obfuscate` cannot be used together (native code is already opaque)

### Optimization

| Flag | Description |
|------|-------------|
| `--optimize` | Optimize bundle size: strips debug symbols from binaries, prunes unused stdlib modules, removes `.dist-info` metadata |

## Build pipeline

The build process runs through six phases:

1. **Setup** -- Locates the `nib-runtime` Swift executable and detects third-party dependencies via AST analysis of your script. Dependencies listed in `[project].dependencies` in `pyproject.toml` take precedence over auto-detection.

2. **Python environment** -- Downloads a portable [python-build-standalone](https://github.com/astral-sh/python-build-standalone) distribution (cached in `~/.cache/nib/`), extracts it, and vendors all dependencies with `pip install --target`.

3. **Copy code** -- Copies your script, sibling `.py` files, local packages, and the `assets/` directory into the bundle. Fonts in `assets/` are automatically registered.

4. **Compile** -- Compiles Python to bytecode (`.pyc`), native modules (`.so`), or leaves source as-is depending on flags.

5. **Finalize** -- Installs the Swift runtime as the main executable, converts the icon to `.icns` format, and generates `Info.plist` from your configuration.

6. **Cleanup and sign** -- Prunes the Python distribution (removes test suites, idle, tkinter, etc.), optionally strips binaries, and applies an ad-hoc code signature.

## Bundle structure

```
My App.app/
└── Contents/
    ├── Info.plist
    ├── MacOS/
    │   └── My App              # Swift runtime (main executable)
    └── Resources/
        ├── app/
        │   ├── main.pyc         # Your compiled application code
        │   └── vendor/          # Vendored dependencies + nib SDK
        ├── assets/              # Your assets (icons, images, fonts)
        └── python/              # Embedded Python distribution
```

## Examples

Build with defaults from `pyproject.toml`:

```bash
nib build
```

Build with a custom name and icon:

```bash
nib build src/main.py --name "Weather Widget" --icon src/assets/icon.png
```

Build with native compilation for maximum code protection:

```bash
nib build --native
```

!!! note "Cython required"
    The `--native` flag requires Cython to be installed: `pip install cython`

Build an optimized, obfuscated release:

```bash
nib build --obfuscate --optimize
```

Build for a specific architecture:

```bash
nib build --arch x86_64
```

Build with additional dependencies that auto-detection missed:

```bash
nib build --extra-deps "pillow,scipy"
```

## Configuration precedence

When both CLI arguments and `pyproject.toml` settings are present, CLI arguments take precedence:

1. Command-line arguments (highest priority)
2. `[tool.nib.build]` section in `pyproject.toml`
3. Default values

See the [pyproject.toml configuration](pyproject-config.md) reference for all available settings.
