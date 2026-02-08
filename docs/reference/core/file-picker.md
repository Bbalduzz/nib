# FilePicker

Native macOS file picker dialogs for selecting and saving files. Wraps `NSOpenPanel` and `NSSavePanel` with full access to their configuration options. All methods are **synchronous** and block until the user makes a selection or cancels.

## Constructor

```python
nib.FilePicker(app=None)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app` | `App \| None` | `None` | The App instance to use. If `None`, uses the current running app set by `nib.run()` |

## Methods

### `pick_files(...)`

Open a file selection dialog. Returns a list of `PickedFile` objects, or `None` if the user cancels.

```python
picker.pick_files(
    *,
    multiple=False,
    extensions=None,
    uttypes=None,
    directory=None,
    title="Select Files",
    message=None,
    button_label="Open",
    shows_hidden_files=False,
    resolves_aliases=True,
    allows_other_file_types=False,
    treats_packages_as_directories=False,
    validator=None,
) -> list[PickedFile] | None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `multiple` | `bool` | `False` | Allow selecting multiple files |
| `extensions` | `list[str] \| None` | `None` | Allowed file extensions, e.g. `["png", "jpg", "gif"]` |
| `uttypes` | `list[str] \| None` | `None` | Allowed Uniform Type Identifiers, e.g. `["public.image"]` |
| `directory` | `str \| None` | `None` | Initial directory path to open the dialog in |
| `title` | `str` | `"Select Files"` | Dialog window title |
| `message` | `str \| None` | `None` | Prompt text displayed below the title bar |
| `button_label` | `str` | `"Open"` | Text for the confirmation button |
| `shows_hidden_files` | `bool` | `False` | Show hidden files (dotfiles) in the dialog |
| `resolves_aliases` | `bool` | `True` | Follow macOS alias files to their targets |
| `allows_other_file_types` | `bool` | `False` | Allow files outside the specified `extensions` / `uttypes` |
| `treats_packages_as_directories` | `bool` | `False` | Show `.app` bundles and packages as browsable folders |
| `validator` | `Callable[[list[str]], str \| None] \| None` | `None` | Validation function. Receives a list of selected paths. Return `None` if valid, or an error message string to reject the selection |

### `pick_directory(...)`

Open a directory selection dialog. Returns a list of directory path strings, or `None` if cancelled.

```python
picker.pick_directory(
    *,
    multiple=False,
    directory=None,
    title="Select Folder",
    message=None,
    button_label="Select",
    shows_hidden_files=False,
    resolves_aliases=True,
    can_create_directories=True,
    validator=None,
) -> list[str] | None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `multiple` | `bool` | `False` | Allow selecting multiple directories |
| `directory` | `str \| None` | `None` | Initial directory path |
| `title` | `str` | `"Select Folder"` | Dialog window title |
| `message` | `str \| None` | `None` | Prompt text below the title bar |
| `button_label` | `str` | `"Select"` | Text for the confirmation button |
| `shows_hidden_files` | `bool` | `False` | Show hidden files |
| `resolves_aliases` | `bool` | `True` | Follow alias files |
| `can_create_directories` | `bool` | `True` | Allow creating new folders in the dialog |
| `validator` | `Callable[[list[str]], str \| None] \| None` | `None` | Validation function. Receives selected directory paths. Return `None` if valid, or an error message to reject |

### `save_file(...)`

Open a save file dialog. Returns a `SaveResult`, or `None` if cancelled.

```python
picker.save_file(
    *,
    filename=None,
    extensions=None,
    uttypes=None,
    directory=None,
    title="Save File",
    message=None,
    button_label="Save",
    name_field_label="Save As:",
    shows_hidden_files=False,
    can_create_directories=True,
    allows_other_file_types=False,
    shows_tag_field=True,
    validator=None,
) -> SaveResult | None
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `filename` | `str \| None` | `None` | Suggested filename pre-filled in the dialog |
| `extensions` | `list[str] \| None` | `None` | Allowed file extensions |
| `uttypes` | `list[str] \| None` | `None` | Allowed Uniform Type Identifiers |
| `directory` | `str \| None` | `None` | Initial directory path |
| `title` | `str` | `"Save File"` | Dialog window title |
| `message` | `str \| None` | `None` | Prompt text below the title bar |
| `button_label` | `str` | `"Save"` | Text for the save button |
| `name_field_label` | `str` | `"Save As:"` | Label for the filename text field |
| `shows_hidden_files` | `bool` | `False` | Show hidden files |
| `can_create_directories` | `bool` | `True` | Allow creating new folders |
| `allows_other_file_types` | `bool` | `False` | Allow extensions outside the allowed list |
| `shows_tag_field` | `bool` | `True` | Show the macOS Finder tags selector |
| `validator` | `Callable[[str], str \| None] \| None` | `None` | Validation function. Receives the chosen path. Return `None` if valid, or an error message to reject |

---

## Data Classes

### PickedFile

Represents a file selected by the user.

```python
@dataclass
class PickedFile:
    name: str
    path: str
    size: int
    uti: str | None
    tags: list[str]
```

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Filename, e.g. `"photo.png"` |
| `path` | `str` | Full absolute file path |
| `size` | `int` | File size in bytes |
| `uti` | `str \| None` | Uniform Type Identifier, e.g. `"public.png"` |
| `tags` | `list[str]` | macOS Finder tags assigned to the file |

### SaveResult

Result from a save file dialog.

```python
@dataclass
class SaveResult:
    path: str
    tags: list[str]
```

| Field | Type | Description |
|---|---|---|
| `path` | `str` | The chosen save path |
| `tags` | `list[str]` | Finder tags selected by the user in the dialog |

---

## Examples

### Picking image files

```python
import nib

def main(app: nib.App):
    app.title = "Image Picker"
    app.icon = nib.SFSymbol("photo")
    app.width = 350
    app.height = 200

    result_label = nib.Text("No file selected", font=nib.Font.BODY)
    picker = nib.FilePicker()

    def select_images():
        files = picker.pick_files(
            multiple=True,
            extensions=["png", "jpg", "jpeg", "gif"],
            title="Select Images",
            message="Choose one or more image files",
        )
        if files:
            names = ", ".join(f.name for f in files)
            total_size = sum(f.size for f in files)
            result_label.content = f"{len(files)} files ({total_size} bytes): {names}"
        else:
            result_label.content = "Selection cancelled"

    app.build(
        nib.VStack(
            controls=[
                result_label,
                nib.Button("Select Images", action=select_images),
            ],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Saving a file

```python
import nib

def main(app: nib.App):
    app.title = "Save Demo"
    app.icon = nib.SFSymbol("square.and.arrow.down")
    app.width = 350
    app.height = 150

    info = nib.Text("Click save to choose a location", font=nib.Font.BODY)
    picker = nib.FilePicker()

    def save():
        result = picker.save_file(
            filename="report.txt",
            extensions=["txt", "md"],
            title="Save Report",
            message="Choose where to save the report",
        )
        if result:
            info.content = f"Saved to: {result.path}"
            # Write the file
            with open(result.path, "w") as f:
                f.write("Hello from Nib!")
        else:
            info.content = "Save cancelled"

    app.build(
        nib.VStack(
            controls=[info, nib.Button("Save Report", action=save)],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

### Picking a directory

```python
import nib
import os

def main(app: nib.App):
    app.title = "Folder Picker"
    app.icon = nib.SFSymbol("folder")
    app.width = 400
    app.height = 200

    info = nib.Text("No folder selected")
    picker = nib.FilePicker()

    def select_folder():
        dirs = picker.pick_directory(
            title="Select Output Folder",
            message="Files will be exported here",
            can_create_directories=True,
        )
        if dirs:
            path = dirs[0]
            file_count = len(os.listdir(path))
            info.content = f"Selected: {path} ({file_count} items)"
        else:
            info.content = "No folder selected"

    app.build(
        nib.VStack(
            controls=[info, nib.Button("Choose Folder", action=select_folder)],
            spacing=12,
            padding=20,
        )
    )

nib.run(main)
```

## Related

- [App](app.md) -- The `app.open_file_dialog()` and `app.save_file_dialog()` convenience methods
- [UserDefaults](user-defaults.md) -- For persisting file paths or recent selections
