# Installation

## Requirements

Nib requires:

| Requirement | Minimum version |
|-------------|-----------------|
| **macOS**   | 14 (Sonoma)+    |
| **Python**  | 3.10+           |

!!! note
    Nib apps are macOS-only. The framework relies on SwiftUI for rendering and system APIs that are exclusive to Apple platforms.

## Install via pip

The recommended way to install Nib is from PyPI:

```bash
pip install pynib
```

This installs the Python SDK **and** the pre-built Swift runtime binary. No Xcode or Swift toolchain required.

## Verify the installation

After installing, confirm that the CLI is available:

```bash
nib -h
```

You should see output like:

```bash
usage: nib [-h] [-v] {create,build,run} ...

Nib - Build macOS menu bar apps with Python

positional arguments:
  {create,build,run}  Available commands
    create            Create a new nib project
    build             Build a standalone .app bundle
    run               Run a nib app with hot reload

options:
  -h, --help          show this help message and exit
  -v, --verbose       Enable verbose output
```

!!! tip
    If `nib` is not found, make sure the Python `bin` directory is on your `PATH`. When using a virtual environment, activate it first.

## Using a virtual environment

It is good practice to install Nib inside a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pynib
```

## Building from source

If you want to contribute to Nib or need the latest unreleased changes, you can build from source.

### 1. Clone the repository

```bash
git clone https://github.com/Bbalduzz/nib.git
cd nib
```

### 2. Build the Swift runtime and install

The `make install` command builds the universal Swift runtime binary (arm64 + x86_64) and installs the Python package in editable mode:

```bash
make install
```

This runs two steps under the hood:

1. **Build the Swift runtime** -- Compiles the Swift package in release mode and copies the `nib-runtime` binary into the Python SDK.
2. **Install the Python SDK** -- Runs `pip install -e .` so that changes to the Python code are reflected immediately.

!!! warning
    Building from source requires Xcode and the Swift toolchain. You can install Xcode from the Mac App Store or use the Xcode Command Line Tools (`xcode-select --install`).

### Build the runtime only

If you only need to rebuild the Swift side without reinstalling the Python package:

```bash
make build-runtime
```

The compiled binary lands at `sdk/python/nib/bin/nib-runtime`.

## Next steps

With Nib installed, head to the [Quick Start](quickstart.md) to create and run your first project.
