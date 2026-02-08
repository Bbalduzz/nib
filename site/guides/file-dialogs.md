# File Dialogs

Nib provides native macOS file dialogs (NSOpenPanel and NSSavePanel) through the `FilePicker` class. You can pick files, pick directories, and save files -- all with full access to dialog options like file type filtering, hidden file visibility, and Finder tag support.

## Creating a FilePicker

```python
import nib

picker = nib.FilePicker()
```

The `FilePicker` automatically uses the current running app instance. You can also pass an explicit `App` reference:

```python
picker = nib.FilePicker(app)
```

!!! note
    All `FilePicker` methods are **blocking** -- they pause execution until the user selects a file or cancels the dialog, then return the result directly. No callbacks needed.

## Picking files

Use `pick_files()` to open a file selection dialog:

```python
files = picker.pick_files(
    extensions=["txt", "md"],
    title="Select Text Files",
)

if files:
    for f in files:
        print(f"Name: {f.name}")
        print(f"Path: {f.path}")
        print(f"Size: {f.size} bytes")
```

The method returns a list of `PickedFile` objects, or `None` if the user cancelled.

### Selecting multiple files

```python
files = picker.pick_files(
    extensions=["png", "jpg", "gif"],
    multiple=True,
    title="Select Images",
)

if files:
    print(f"Selected {len(files)} file(s)")
```

### Full parameter list

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `multiple` | `bool` | `False` | Allow selecting multiple files |
| `extensions` | `list[str]` | `None` | Allowed file extensions (e.g., `["png", "jpg"]`) |
| `uttypes` | `list[str]` | `None` | Allowed Uniform Type Identifiers (e.g., `["public.image"]`) |
| `directory` | `str` | `None` | Initial directory path |
| `title` | `str` | `"Select Files"` | Dialog window title |
| `message` | `str` | `None` | Prompt text shown below the title |
| `button_label` | `str` | `"Open"` | Text for the OK button |
| `shows_hidden_files` | `bool` | `False` | Show hidden files in the dialog |
| `resolves_aliases` | `bool` | `True` | Follow alias files to their targets |
| `allows_other_file_types` | `bool` | `False` | Allow files outside the allowed types |
| `treats_packages_as_directories` | `bool` | `False` | Treat `.app` bundles as folders |
| `validator` | `Callable` | `None` | Validation function (see below) |

### PickedFile dataclass

Each selected file is returned as a `PickedFile` with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Filename (e.g., `"document.txt"`) |
| `path` | `str` | Absolute file path |
| `size` | `int` | File size in bytes |
| `uti` | `str` or `None` | Uniform Type Identifier (e.g., `"public.plain-text"`) |
| `tags` | `list[str]` | macOS Finder tags |

## Picking a directory

Use `pick_directory()` to let the user choose a folder:

```python
dirs = picker.pick_directory(title="Select Output Folder")

if dirs:
    output_dir = dirs[0]
    print(f"Selected: {output_dir}")
```

The method returns a list of directory path strings, or `None` if cancelled.

### Multiple directories

```python
dirs = picker.pick_directory(
    multiple=True,
    title="Select Folders to Scan",
)
```

### Full parameter list

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `multiple` | `bool` | `False` | Allow selecting multiple directories |
| `directory` | `str` | `None` | Initial directory path |
| `title` | `str` | `"Select Folder"` | Dialog window title |
| `message` | `str` | `None` | Prompt text shown below the title |
| `button_label` | `str` | `"Select"` | Text for the OK button |
| `shows_hidden_files` | `bool` | `False` | Show hidden files |
| `resolves_aliases` | `bool` | `True` | Follow aliases to targets |
| `can_create_directories` | `bool` | `True` | Allow creating new folders |
| `validator` | `Callable` | `None` | Validation function |

## Saving a file

Use `save_file()` to show a save dialog:

```python
result = picker.save_file(
    filename="output.txt",
    extensions=["txt"],
    title="Save Report",
)

if result:
    print(f"Save to: {result.path}")
    print(f"Tags: {result.tags}")
```

The method returns a `SaveResult` object, or `None` if cancelled.

### Full parameter list

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | `None` | Suggested filename |
| `extensions` | `list[str]` | `None` | Allowed file extensions |
| `uttypes` | `list[str]` | `None` | Allowed Uniform Type Identifiers |
| `directory` | `str` | `None` | Initial directory path |
| `title` | `str` | `"Save File"` | Dialog window title |
| `message` | `str` | `None` | Prompt text shown below the title |
| `button_label` | `str` | `"Save"` | Text for the Save button |
| `name_field_label` | `str` | `"Save As:"` | Label for the filename field |
| `shows_hidden_files` | `bool` | `False` | Show hidden files |
| `can_create_directories` | `bool` | `True` | Allow creating new folders |
| `allows_other_file_types` | `bool` | `False` | Allow extensions outside the allowed list |
| `shows_tag_field` | `bool` | `True` | Show the Finder tags selector |
| `validator` | `Callable` | `None` | Validation function |

### SaveResult dataclass

| Field | Type | Description |
|-------|------|-------------|
| `path` | `str` | The chosen save path |
| `tags` | `list[str]` | User-selected Finder tags |

## Validation

All three methods accept a `validator` parameter. The validator is a function that receives the selected path(s) and returns `None` if valid, or an error message string if invalid:

```python
def validate_size(paths: list[str]) -> str | None:
    import os
    for path in paths:
        if os.path.getsize(path) > 10_000_000:
            return "File must be under 10 MB"
    return None

files = picker.pick_files(
    extensions=["csv"],
    validator=validate_size,
)
```

For `save_file()`, the validator receives a single path string instead of a list:

```python
def validate_save(path: str) -> str | None:
    if path.endswith(".system"):
        return "Cannot overwrite system files"
    return None

result = picker.save_file(validator=validate_save)
```

## App-level shortcuts

The `App` class also provides shortcut methods for file dialogs that use a callback-based pattern:

```python
def main(app: nib.App):
    def handle_file(path):
        print(f"Selected: {path}")

    def handle_save(path):
        print(f"Save to: {path}")

    app.build(
        nib.VStack(
            controls=[
                nib.Button("Open File", action=lambda: app.open_file_dialog(
                    callback=handle_file,
                    types=["txt", "md"],
                )),
                nib.Button("Save File", action=lambda: app.save_file_dialog(
                    callback=handle_save,
                )),
            ],
            spacing=8,
            padding=16,
        )
    )
```

!!! tip
    Prefer the `FilePicker` class for new code. It provides a more complete API with blocking semantics that are easier to work with.

## Complete example

A file viewer app that lets you open text files and display their contents:

```python
import nib


def main(app: nib.App):
    app.title = "File Viewer"
    app.icon = nib.SFSymbol("doc.text")
    app.width = 400
    app.height = 500

    picker = nib.FilePicker()

    file_name = nib.Text("No file selected", font=nib.Font.HEADLINE)
    file_content = nib.Text("", font=nib.Font.system(12))
    file_size = nib.Text("", foreground_color=nib.Color.GRAY)

    def open_file():
        files = picker.pick_files(
            extensions=["txt", "md", "py", "json"],
            title="Open Text File",
            message="Choose a file to view",
        )
        if files:
            f = files[0]
            file_name.content = f.name
            file_size.content = f"{f.size:,} bytes"
            try:
                with open(f.path, "r") as fh:
                    file_content.content = fh.read()
            except Exception as e:
                file_content.content = f"Error reading file: {e}"

    def save_file():
        if not file_content.content:
            return
        result = picker.save_file(
            filename="copy.txt",
            extensions=["txt"],
            title="Save Copy",
        )
        if result:
            with open(result.path, "w") as fh:
                fh.write(file_content.content)
            app.notify("Saved", f"File saved to {result.path}")

    app.build(
        nib.VStack(
            controls=[
                nib.HStack(
                    controls=[
                        file_name,
                        nib.Spacer(),
                        file_size,
                    ],
                ),
                nib.Divider(),
                nib.ScrollView(
                    controls=[file_content],
                ),
                nib.HStack(
                    controls=[
                        nib.Button("Open", action=open_file),
                        nib.Button("Save Copy", action=save_file),
                    ],
                    spacing=8,
                ),
            ],
            spacing=8,
            padding=16,
        )
    )


nib.run(main)
```
