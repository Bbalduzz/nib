# nib run

Run a Nib application in development mode with automatic hot reload on file changes.

## Usage

```bash
nib run [script.py] [-r] [-v]
```

If no script is specified, `nib run` reads the entry point from `pyproject.toml`:

```bash
nib run                  # Uses [tool.nib] entry (defaults to src/main.py)
nib run src/main.py      # Explicit script path
nib run my_project/      # Runs my_project/src/main.py (enables recursive watching)
```

## Options

| Flag | Description |
|------|-------------|
| `-r`, `--recursive` | Watch subdirectories for changes |
| `-v`, `--verbose` | Enable verbose output (show info-level logs) |

## How it works

When you run `nib run`, the following happens:

1. The Swift runtime (`nib-runtime`) is launched as a separate process
2. A Unix socket connection is established between Python and Swift
3. Your Python script is executed and the UI is rendered
4. A file watcher monitors `.py` files for changes

On every file save, only the Python side restarts -- the Swift runtime stays alive. This means the menu bar icon persists and UI updates are near-instant.

```
Save file --> Python reloads --> new UI sent to Swift runtime (still running)
```

## Hot reload

The watcher triggers a reload whenever a `.py` file is modified. The reload process:

1. Clears cached user modules from `sys.modules`
2. Re-executes your script from scratch
3. Sends the updated view tree to the Swift runtime

!!! info "Debouncing"
    Rapid saves are coalesced with a 100ms debounce window. If you save multiple times in quick succession, only one reload is triggered.

### Excluded directories

The watcher ignores changes in these directories:

- `__pycache__`
- `.git`
- `.venv`, `venv`
- `node_modules`
- `.mypy_cache`, `.pytest_cache`, `.ruff_cache`
- `dist`, `build`
- `.eggs`

### Recursive watching

By default, only the script's parent directory is watched (non-recursively). Use `-r` to watch all subdirectories:

```bash
nib run src/main.py -r    # Watches src/ and all its subdirectories
```

When you pass a directory instead of a script, recursive watching is enabled automatically:

```bash
nib run my_project/       # Equivalent to: nib run my_project/src/main.py -r
```

## Error handling

Syntax errors and runtime exceptions are displayed in the terminal. The Swift runtime keeps running, so you can fix the error and save to trigger another reload.

```
$ nib run
File changed: main.py
Reloading...
Syntax error in /path/to/main.py:12
    if True
          ^
  expected ':'
Fix the error and save to reload...
```

No need to restart -- just fix the problem and save.

## Stopping

Press `Ctrl+C` to stop both the Python process and the Swift runtime. The Unix socket is cleaned up automatically.
