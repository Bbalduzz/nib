# CLI Reference

Nib provides a command-line interface with three commands for the full development lifecycle of a macOS menu bar application.

| Command | Description |
|---------|-------------|
| [`nib create`](create.md) | Scaffold a new project with standard structure |
| [`nib run`](run.md) | Run your app in development mode with hot reload |
| [`nib build`](build.md) | Build a standalone `.app` bundle for distribution |

All commands support `-v` / `--verbose` for detailed output.

## Configuration

Commands read defaults from `pyproject.toml` when present. See the [pyproject.toml configuration](pyproject-config.md) reference for all available options.

## Quick start

```bash
nib create my-app        # Scaffold a new project
cd my_app
nib run                  # Run with hot reload (reads entry from pyproject.toml)
nib build                # Build standalone .app bundle
```
