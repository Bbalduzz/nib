TextEditor
==========

A multi-line text editing view for longer text input.

.. code-block:: python

    import nib

    editor = nib.TextEditor(
        text="Initial content...",
        placeholder="Enter your notes here",
    )

Parameters
----------

text : str
    Initial text content.

placeholder : str, optional
    Placeholder text shown when empty.

on_change : callable, optional
    Callback called when text changes. Receives the new text as argument.

style : TextStyle, optional
    Text style configuration for font, color, and formatting.

font : Font, optional
    Text font (alternative to using style).

foreground_color : Color or str, optional
    Text color (alternative to using style).

line_limit : int, optional
    Maximum number of lines.

scrolls_disabled : bool, optional
    Whether scrolling is disabled (default: False).

content_background : Color, str, or bool, optional
    Background color for the text content area.

    - ``None``: Use system default background (default)
    - ``False`` or ``"hidden"``: Hide the default background (transparent)
    - Color or string: Use specified color as background

Using TextStyle
---------------

Apply consistent text styling with ``TextStyle``:

.. code-block:: python

    # Using a preset style
    editor = nib.TextEditor(
        text="",
        style=nib.TextStyle.BODY,
    )

    # Using a custom style
    code_editor = nib.TextEditor(
        text="def hello():\n    print('world')",
        style=nib.TextStyle(
            font=nib.Font.system(14),
            monospaced=True,
        ),
    )

    # Style with color
    styled_editor = nib.TextEditor(
        text="Important notes...",
        style=nib.TextStyle(
            font=nib.Font.BODY,
            color=nib.Color.PRIMARY,
        ),
    )

.. note::

    TextEditor supports a subset of TextStyle options. The ``monospaced`` style
    works well for code editing. Other decorations like bold, italic, underline
    are not supported by SwiftUI's TextEditor.

Custom Background
-----------------

Remove or customize the default TextEditor background:

.. code-block:: python

    # Transparent background (hide default)
    editor = nib.TextEditor(
        text="",
        content_background=False,  # or "hidden"
    )

    # Custom background color
    editor = nib.TextEditor(
        text="",
        content_background=nib.Color.SECONDARY.opacity(0.1),
    )

    # With outer background view
    editor = nib.TextEditor(
        text="",
        content_background=False,
        background=nib.RoundedRectangle(
            corner_radius=8,
            fill=nib.Color.SECONDARY.opacity(0.1),
        ),
    )

.. note::

    The ``content_background`` parameter requires macOS 14+. On older systems,
    the default background cannot be hidden.

Example: Note Taking
--------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "Notes"
        app.width = 400
        app.height = 300

        notes = nib.TextEditor(
            text="",
            placeholder="Write your notes here...",
            style=nib.TextStyle.BODY,
        )

        def on_text_change(new_text: str):
            print(f"Text changed: {len(new_text)} characters")

        notes.on_change = on_text_change

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("My Notes", font=nib.Font.title),
                    notes,
                ],
                spacing=12,
                padding=16,
            )
        )

    nib.run(main)

Updating Content
----------------

You can update the text content programmatically:

.. code-block:: python

    editor = nib.TextEditor(text="")

    def load_content():
        editor.text = "Loaded content from file..."

    def clear():
        editor.text = ""

Difference from TextField
-------------------------

- **TextField**: Single-line input, suitable for short text like names, emails, passwords
- **TextEditor**: Multi-line input, suitable for longer text like notes, descriptions, code
