# Todo App

A task list application that demonstrates text input, dynamic list rendering, toggles for marking tasks complete, and deleting items from the view tree.

## Full Source

```python
import nib

def main(app: nib.App):
    app.title = "Todo"
    app.icon = nib.SFSymbol("checklist")
    app.width = 340
    app.height = 450

    # State
    todos = []  # list of {"text": str, "done": bool, "views": dict}
    todo_section = nib.Section(header="Tasks", controls=[])
    done_section = nib.Section(header="Completed", controls=[])
    input_field = nib.TextField(placeholder="What needs to be done?", on_submit=lambda _: add_todo())

    def rebuild_lists():
        """Rebuild both sections from the todos list."""
        pending = [t for t in todos if not t["done"]]
        completed = [t for t in todos if t["done"]]

        todo_section.controls = [make_row(t) for t in pending]
        done_section.controls = [make_row(t) for t in completed]

    def make_row(todo):
        """Create a view row for a single todo item."""
        def toggle_done(is_on):
            todo["done"] = is_on
            rebuild_lists()

        def delete():
            todos.remove(todo)
            rebuild_lists()

        return nib.HStack(
            controls=[
                nib.Toggle(
                    is_on=todo["done"],
                    label="",
                    on_change=toggle_done,
                ),
                nib.Text(
                    todo["text"],
                    foreground_color=nib.Color.SECONDARY if todo["done"] else nib.Color.PRIMARY,
                ),
                nib.Spacer(),
                nib.Button(
                    icon="trash",
                    action=delete,
                    role=nib.ButtonRole.DESTRUCTIVE,
                    style=nib.ButtonStyle.BORDERLESS,
                ),
            ],
            spacing=8,
        )

    def add_todo():
        text = input_field.text.strip()
        if text:
            todos.append({"text": text, "done": False})
            input_field.text = ""
            rebuild_lists()

    def clear_completed():
        nonlocal todos
        todos = [t for t in todos if not t["done"]]
        rebuild_lists()

    # Context menu
    app.menu = [
        nib.MenuItem("Clear Completed", action=clear_completed, icon="trash"),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit, shortcut="cmd+q"),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Todo", font=nib.Font.TITLE),
                nib.HStack(
                    controls=[
                        input_field,
                        nib.Button(
                            "Add",
                            action=add_todo,
                            style=nib.ButtonStyle.BORDERED_PROMINENT,
                        ),
                    ],
                    spacing=8,
                ),
                nib.Divider(),
                nib.ScrollView(
                    controls=[
                        nib.VStack(
                            controls=[todo_section, done_section],
                            spacing=12,
                        ),
                    ],
                ),
            ],
            spacing=12,
            padding=16,
        )
    )

nib.run(main)
```

## Walkthrough

### Data model

```python
todos = []  # list of {"text": str, "done": bool}
```

The app uses a plain Python list of dictionaries as its data model. Each todo has a `text` string and a `done` boolean. There is no ORM or special state container needed -- Nib's reactivity triggers when you reassign view properties.

### Text input and submission

```python
input_field = nib.TextField(placeholder="What needs to be done?", on_submit=lambda _: add_todo())
```

`TextField` provides a text input with an `on_submit` callback that fires when the user presses Enter. The `text` property can be read to get the current value and written to clear the field after adding a todo.

### Dynamic list rendering

```python
def rebuild_lists():
    pending = [t for t in todos if not t["done"]]
    completed = [t for t in todos if t["done"]]

    todo_section.controls = [make_row(t) for t in pending]
    done_section.controls = [make_row(t) for t in completed]
```

When the data changes, the `rebuild_lists` function partitions the todos into pending and completed, then reassigns the `controls` property on each `Section`. Nib diffs the old and new view trees and patches only the changed nodes.

### Row factory

```python
def make_row(todo):
    def toggle_done(is_on):
        todo["done"] = is_on
        rebuild_lists()

    def delete():
        todos.remove(todo)
        rebuild_lists()

    return nib.HStack(
        controls=[
            nib.Toggle(is_on=todo["done"], label="", on_change=toggle_done),
            nib.Text(todo["text"], ...),
            nib.Spacer(),
            nib.Button(icon="trash", action=delete, ...),
        ],
        spacing=8,
    )
```

Each row is an `HStack` containing:

- A `Toggle` checkbox that marks the task as complete
- A `Text` label with conditional styling (secondary color when done)
- A `Spacer` to push the delete button to the right edge
- A destructive icon-only `Button` for deletion

The callbacks use closures to capture the specific `todo` dictionary, so each row manipulates the correct item.

### Layout structure

The main layout uses a `VStack` with:

- A title text
- An input row (`HStack` with `TextField` and `Button`)
- A `Divider` separator
- A `ScrollView` containing the two `Section` groups

The `ScrollView` ensures the list is scrollable when there are many items. The `Section` views group tasks under "Tasks" and "Completed" headers.

### Running

```bash
nib run todo.py
```
