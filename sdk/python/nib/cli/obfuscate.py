"""Custom bytecode obfuscator for Nib applications.

This module provides bytecode obfuscation that works with Python's module
import system, unlike pyc-zipper which adds an exec() wrapper.

Obfuscates:
- co_filename: Source file path -> empty string
- co_name: Function/class names -> empty string
- co_firstlineno: Line number -> 1
- co_linetable/co_lnotab: Line mapping -> empty bytes
- co_varnames: Local variable names -> numbered (0, 1, 2...)

Does NOT touch (to preserve functionality):
- co_names: Global/attribute names (would break imports)
- co_freevars/co_cellvars: Closure variables (must stay in sync)
"""

import marshal
import sys
import types
from pathlib import Path


def obfuscate_code(code: types.CodeType, obfuscate_varnames: bool = False) -> types.CodeType:
    """Recursively obfuscate a code object.

    Args:
        code: The code object to obfuscate.
        obfuscate_varnames: Whether to rename local variables (can break kwargs).

    Returns:
        A new code object with obfuscated attributes.
    """
    # Obfuscate nested code objects first (functions, classes, lambdas)
    new_consts = []
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            new_consts.append(obfuscate_code(const, obfuscate_varnames))
        else:
            new_consts.append(const)

    # Build kwargs for code.replace()
    # Different Python versions have different attributes
    kwargs = {
        "co_filename": "",  # Strip source path
        "co_name": "",  # Strip function/class name
        "co_firstlineno": 1,  # Reset line number
        "co_consts": tuple(new_consts),
    }

    # Optionally rename local variables (disabled by default - can break kwargs)
    if obfuscate_varnames:
        kwargs["co_varnames"] = tuple(str(i) for i in range(len(code.co_varnames)))

    # Handle line table (version-dependent)
    if sys.version_info >= (3, 10):
        # Python 3.10+ uses co_linetable
        kwargs["co_linetable"] = b""
    else:
        # Python 3.8-3.9 uses co_lnotab
        kwargs["co_lnotab"] = b""

    # Python 3.11+ has co_qualname
    if sys.version_info >= (3, 11):
        kwargs["co_qualname"] = ""

    return code.replace(**kwargs)


def obfuscate_pyc(pyc_path: Path) -> None:
    """Obfuscate a .pyc file in place.

    Args:
        pyc_path: Path to the .pyc file to obfuscate.

    Raises:
        Exception: If the file cannot be read or written.
    """
    with open(pyc_path, "rb") as f:
        # .pyc header structure (Python 3.7+):
        # - 4 bytes: magic number
        # - 4 bytes: bit field (PEP 552)
        # - 4 bytes: timestamp or hash
        # - 4 bytes: source size
        # Total: 16 bytes
        header = f.read(16)
        code = marshal.load(f)

    # Obfuscate the code object
    new_code = obfuscate_code(code)

    # Write back
    with open(pyc_path, "wb") as f:
        f.write(header)
        marshal.dump(new_code, f)


def obfuscate_directory(directory: Path) -> tuple[int, int]:
    """Obfuscate all .pyc files in a directory.

    Args:
        directory: Path to the directory containing .pyc files.

    Returns:
        Tuple of (success_count, failure_count).
    """
    success = 0
    failures = 0

    for pyc_file in directory.rglob("*.pyc"):
        try:
            obfuscate_pyc(pyc_file)
            success += 1
        except Exception:
            failures += 1

    return success, failures
