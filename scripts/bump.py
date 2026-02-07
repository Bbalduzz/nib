"""Bump the version in sdk/python/nib/__init__.py."""

import re
import sys
from pathlib import Path

VERSION_FILE = Path(__file__).parent.parent / "sdk/python/nib/__init__.py"
PATTERN = re.compile(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"')


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("patch", "minor", "major"):
        print("Usage: python scripts/bump.py [patch|minor|major]")
        sys.exit(1)

    part = sys.argv[1]
    text = VERSION_FILE.read_text()
    match = PATTERN.search(text)
    if not match:
        print(f"Could not find __version__ in {VERSION_FILE}")
        sys.exit(1)

    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))

    if part == "patch":
        patch += 1
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0

    new_version = f"{major}.{minor}.{patch}"
    new_text = PATTERN.sub(f'__version__ = "{new_version}"', text)
    VERSION_FILE.write_text(new_text)
    print(f"Bumped to {new_version}")


if __name__ == "__main__":
    main()
