"""Stamp the Python version into Swift's Version.swift before building."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
VERSION_FILE = ROOT / "sdk/python/nib/__init__.py"
SWIFT_VERSION_FILE = ROOT / "package/Nib/Version.swift"

text = VERSION_FILE.read_text()
match = re.search(r'__version__\s*=\s*"(.*?)"', text)
if not match:
    raise SystemExit(f"Could not find __version__ in {VERSION_FILE}")

version = match.group(1)

SWIFT_VERSION_FILE.write_text(
    f'import Foundation\n\nenum NibRuntimeInfo {{\n    static let version = "{version}"\n}}\n'
)

print(f"Stamped Version.swift -> {version}")
