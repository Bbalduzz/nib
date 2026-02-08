# Table

![Table control](../../../assets/img/controls/table.png)

A macOS-native table view for displaying structured data in rows and columns. Table supports column definitions with alignment and width constraints, row selection, sorting callbacks, and double-click handling.

## Constructor

```python
nib.Table(
    columns,
    rows,
    selection=None,
    on_selection=None,
    on_sort=None,
    on_double_click=None,
    row_id_key="id",
    **modifiers,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `columns` | `list[TableColumn]` | *(required)* | List of `TableColumn` definitions specifying the table structure. |
| `rows` | `list[dict]` | *(required)* | List of row data dictionaries. Each dict should contain keys matching the column `key` values and a row identifier. |
| `selection` | `str \| list[str]` | `None` | Currently selected row ID or list of selected row IDs. |
| `on_selection` | `Callable[[list[str]], None]` | `None` | Callback when selection changes. Receives the list of selected row IDs. |
| `on_sort` | `Callable[[str, bool], None]` | `None` | Callback when sort order changes. Receives `(column_id, ascending)`. |
| `on_double_click` | `Callable[[str], None]` | `None` | Callback when a row is double-clicked. Receives the row ID. |
| `row_id_key` | `str` | `"id"` | Key used to identify rows in the data dictionaries. |
| `**modifiers` | | | Common view modifiers: `width`, `height`, `padding`, `background`, etc. |

## TableColumn

```python
nib.TableColumn(
    id,
    title,
    key,
    width=None,
    min_width=None,
    max_width=None,
    alignment="leading",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | `str` | *(required)* | Unique identifier for the column. |
| `title` | `str` | *(required)* | Column header text. |
| `key` | `str` | *(required)* | Key to extract values from row data dictionaries. |
| `width` | `float` | `None` | Fixed column width in points. |
| `min_width` | `float` | `None` | Minimum column width. |
| `max_width` | `float` | `None` | Maximum column width. |
| `alignment` | `str` | `"leading"` | Text alignment. Options: `"leading"`, `"center"`, `"trailing"`. |

## Mutable Properties

| Property | Type | Description |
|----------|------|-------------|
| `columns` | `list[TableColumn]` | Get or set the column definitions. Triggers a UI update. |
| `rows` | `list[dict]` | Get or set the row data. Triggers a UI update. |
| `selection` | `str \| list[str]` | Get or set the selected row ID(s). Triggers a UI update. |

## Examples

### File browser table

```python
import nib

def main(app: nib.App):
    app.build(
        nib.Table(
            columns=[
                nib.TableColumn("name", "Name", "name", min_width=150),
                nib.TableColumn("size", "Size", "size", width=80,
                                 alignment="trailing"),
                nib.TableColumn("date", "Modified", "modified", width=100),
            ],
            rows=[
                {"id": "1", "name": "Document.txt", "size": "4 KB",
                 "modified": "Today"},
                {"id": "2", "name": "Image.png", "size": "1.2 MB",
                 "modified": "Yesterday"},
                {"id": "3", "name": "Archive.zip", "size": "45 MB",
                 "modified": "Last week"},
            ],
            on_selection=lambda ids: print(f"Selected: {ids}"),
            width=400,
            height=200,
            padding=16,
        )
    )

nib.run(main)
```

### Table with sorting and double-click

```python
import nib

def main(app: nib.App):
    rows = [
        {"id": "1", "name": "Alice", "score": "95", "grade": "A"},
        {"id": "2", "name": "Bob", "score": "87", "grade": "B+"},
        {"id": "3", "name": "Carol", "score": "92", "grade": "A-"},
    ]

    table = nib.Table(
        columns=[
            nib.TableColumn("name", "Student", "name", min_width=120),
            nib.TableColumn("score", "Score", "score", width=60,
                             alignment="center"),
            nib.TableColumn("grade", "Grade", "grade", width=60,
                             alignment="center"),
        ],
        rows=rows,
        on_sort=lambda col, asc: print(f"Sort by {col}, asc={asc}"),
        on_double_click=lambda rid: print(f"Double-clicked row: {rid}"),
        width=350,
        height=180,
    )

    app.build(
        nib.VStack(controls=[
            nib.Text("Student Grades", style=nib.TextStyle.TITLE),
            table,
        ], spacing=8, padding=16)
    )

nib.run(main)
```

### Dynamic row updates

```python
import nib

def main(app: nib.App):
    table = nib.Table(
        columns=[
            nib.TableColumn("name", "Task", "name", min_width=150),
            nib.TableColumn("status", "Status", "status", width=80),
        ],
        rows=[
            {"id": "1", "name": "Design", "status": "Done"},
            {"id": "2", "name": "Develop", "status": "In Progress"},
        ],
        width=300,
        height=150,
    )

    count = [3]

    def add_task():
        table.rows = table.rows + [
            {"id": str(count[0]), "name": f"Task {count[0]}",
             "status": "New"}
        ]
        count[0] += 1

    app.build(
        nib.VStack(controls=[
            table,
            nib.Button("Add Task", action=add_task),
        ], spacing=8, padding=16)
    )

nib.run(main)
```
