# nib create

Scaffold a new Nib project with a standard directory structure, ready to run and build.

## Usage

```bash
nib create <name>
```

The `name` argument accepts spaces, hyphens, or underscores. Nib normalizes it into two forms:

| Input | Display name | Directory name |
|-------|-------------|---------------|
| `my-app` | My App | `my_app` |
| `my_awesome_app` | My Awesome App | `my_awesome_app` |
| `"Weather Widget"` | Weather Widget | `weather_widget` |

## Generated files

```
my_app/
├── src/
│   ├── main.py          # Application entry point (counter example)
│   └── assets/
│       └── .gitkeep     # Placeholder for icons and images
├── pyproject.toml       # Project config with commented build options
└── README.md            # Basic development and build instructions
```

### `src/main.py`

A minimal counter application that demonstrates the function-based API:

```python
import nib

def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star.fill")
    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    counter = nib.Text("0")

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Hello, My App!", font=nib.Font.title),
                counter,
                nib.Button("Click me", action=increment),
            ],
            spacing=16,
            padding=24,
        )
    )

nib.run(main)
```

### `pyproject.toml`

Contains project metadata and a `[tool.nib]` section with all build options commented out. See the [pyproject.toml configuration](pyproject-config.md) reference for details.

### `src/assets/`

Place your app icon (`icon.png` or `icon.icns`) and other assets here. The build command automatically detects `src/assets/icon.png` as the default icon.

## Example output

```
$ nib create my-awesome-app
Creating nib project: My Awesome App
  Created: src/main.py
  Created: pyproject.toml
  Created: README.md
  Created: src/assets/

Project created at: /Users/you/projects/my_awesome_app

Next steps:
  cd my_awesome_app
  python src/main.py    # Run in development
  nib build             # Build standalone app
```

!!! warning
    If the target directory already exists, the command exits with an error to avoid overwriting existing files.

## Next steps

After creating your project:

1. `cd` into the project directory
2. Run `nib run` to start the app with hot reload
3. Edit `src/main.py` to build your UI
4. Place an icon at `src/assets/icon.png` for your app bundle
5. Run `nib build` when ready to distribute
