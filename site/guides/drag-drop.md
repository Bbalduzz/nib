# Drag & Drop

Any container view in Nib supports drag-and-drop file handling through the `on_drop` parameter. When a user drags files or directories from Finder onto your view, Nib invokes your callback with a list of absolute file paths.

## Basic usage

Pass an `on_drop` callback to any container view:

```python
import nib


def main(app: nib.App):
    app.title = "Drop Zone"
    app.icon = nib.SFSymbol("arrow.down.doc")
    app.width = 300
    app.height = 250

    status = nib.Text("Drop files here", foreground_color=nib.Color.GRAY)

    def handle_drop(paths: list[str]):
        status.content = f"Received {len(paths)} file(s)"
        for path in paths:
            print(f"Dropped: {path}")

    app.build(
        nib.VStack(
            controls=[
                nib.SFSymbol("arrow.down.circle", font=nib.Font.system(48)),
                status,
            ],
            spacing=16,
            padding=32,
            on_drop=handle_drop,
            border_color="gray",
            border_width=1,
            corner_radius=12,
        )
    )


nib.run(main)
```

## Callback signature

The `on_drop` callback receives a single argument -- a list of absolute file system path strings:

```python
def handle_drop(paths: list[str]):
    for path in paths:
        print(path)
        # e.g., "/Users/me/Desktop/report.pdf"
```

The paths are absolute and can point to either files or directories.

## Supported container views

The `on_drop` parameter is available on all views that inherit from the base `View` class. Common choices for drop zones include:

- `VStack`, `HStack`, `ZStack`
- `ScrollView`
- `List`
- `Group`
- `Form`

```python
nib.HStack(
    controls=[nib.Text("Drop here")],
    on_drop=handle_drop,
    padding=24,
)
```

## Working with dropped files

### Reading file contents

```python
def handle_drop(paths: list[str]):
    for path in paths:
        if path.endswith(".txt"):
            with open(path, "r") as f:
                content = f.read()
                text_view.content = content
```

### Checking file types

```python
import os

def handle_drop(paths: list[str]):
    images = [p for p in paths if p.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
    if images:
        status.content = f"Received {len(images)} image(s)"
    else:
        status.content = "No images found"
```

### Handling directories

```python
import os

def handle_drop(paths: list[str]):
    for path in paths:
        if os.path.isdir(path):
            files = os.listdir(path)
            status.content = f"Folder with {len(files)} items"
        else:
            size = os.path.getsize(path)
            status.content = f"{os.path.basename(path)} ({size:,} bytes)"
```

## Complete example

A file drop zone that displays information about dropped files:

```python
import nib
import os


def main(app: nib.App):
    app.title = "File Info"
    app.icon = nib.SFSymbol("doc.badge.plus")
    app.width = 350
    app.height = 400

    file_list = nib.VStack(controls=[], spacing=4)
    status = nib.Text(
        "Drag files here to inspect",
        foreground_color=nib.Color.GRAY,
        font=nib.Font.CAPTION,
    )

    def handle_drop(paths: list[str]):
        items = []
        for path in paths:
            name = os.path.basename(path)
            if os.path.isdir(path):
                count = len(os.listdir(path))
                items.append(
                    nib.HStack(
                        controls=[
                            nib.SFSymbol("folder.fill", foreground_color="#F59E0B"),
                            nib.VStack(
                                controls=[
                                    nib.Text(name, font=nib.Font.HEADLINE),
                                    nib.Text(
                                        f"{count} items",
                                        font=nib.Font.CAPTION,
                                        foreground_color=nib.Color.GRAY,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=8,
                    )
                )
            else:
                size = os.path.getsize(path)
                ext = os.path.splitext(name)[1].upper() or "FILE"
                items.append(
                    nib.HStack(
                        controls=[
                            nib.SFSymbol("doc.fill", foreground_color="#3B82F6"),
                            nib.VStack(
                                controls=[
                                    nib.Text(name, font=nib.Font.HEADLINE),
                                    nib.Text(
                                        f"{ext} - {size:,} bytes",
                                        font=nib.Font.CAPTION,
                                        foreground_color=nib.Color.GRAY,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=8,
                    )
                )

        status.content = f"{len(paths)} item(s) dropped"
        file_list._children = items
        app.update()

    app.build(
        nib.VStack(
            controls=[
                nib.Text("File Inspector", font=nib.Font.TITLE),
                nib.ScrollView(
                    controls=[file_list],
                ),
                nib.Divider(),
                status,
            ],
            spacing=8,
            padding=16,
            on_drop=handle_drop,
        )
    )


nib.run(main)
```

!!! tip
    The `on_drop` handler runs on the Python side, so you have full access to the file system. You can read files, compute checksums, parse data -- anything Python can do.
