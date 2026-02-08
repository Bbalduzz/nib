Text & Input
============

Views for displaying and editing text.

Text
----

Display static or dynamic text content.

.. code-block:: python

    # Simple text
    nib.Text("Hello, World!")

    # Styled text
    nib.Text(
        "Title",
        font=nib.Font.TITLE,
        foreground_color=nib.Color.BLUE,
    )

    # Reactive text
    label = nib.Text("Count: 0")
    label.content = "Count: 1"  # Triggers re-render

**Parameters:**

- ``content`` - Text to display
- ``font`` - Font style (``Font.TITLE``, ``Font.BODY``, ``Font.CAPTION``, etc.)
- ``foreground_color`` - Text color
- ``line_limit`` - Maximum number of lines (None for unlimited)
- ``multiline_text_alignment`` - Alignment for multi-line text

**Font Presets:**

.. code-block:: python

    nib.Font.LARGE_TITLE
    nib.Font.TITLE
    nib.Font.TITLE2
    nib.Font.TITLE3
    nib.Font.HEADLINE
    nib.Font.BODY
    nib.Font.CALLOUT
    nib.Font.SUBHEADLINE
    nib.Font.FOOTNOTE
    nib.Font.CAPTION
    nib.Font.CAPTION2

    # Custom font
    nib.Font.system(size=16, weight=nib.FontWeight.BOLD)
    nib.Font.custom("SF Mono", size=14)

Attributed Text
~~~~~~~~~~~~~~~

Rich text with inline formatting.

.. code-block:: python

    from nib import AttributedText, TextSpan, TextStyle

    nib.Text(
        content=AttributedText(spans=[
            TextSpan("Bold ", style=TextStyle(font_weight=nib.FontWeight.BOLD)),
            TextSpan("and "),
            TextSpan("Red", style=TextStyle(foreground_color="#FF0000")),
        ])
    )

TextField
---------

Single-line text input.

.. code-block:: python

    def on_change(new_value: str):
        print(f"Value: {new_value}")

    field = nib.TextField(
        value="",
        placeholder="Enter text...",
        on_change=on_change,
    )

    # Read current value
    print(field.value)

    # Set value programmatically
    field.value = "New value"

**Parameters:**

- ``value`` - Current text value
- ``placeholder`` - Placeholder text when empty
- ``on_change`` - Callback when text changes
- ``on_submit`` - Callback when Enter is pressed
- ``text_field_style`` - Style: ``PLAIN``, ``ROUNDED_BORDER``, ``SQUAREBORDER``

SecureField
-----------

Password input with hidden characters.

.. code-block:: python

    nib.SecureField(
        value="",
        placeholder="Enter password",
        on_change=lambda pwd: print(f"Password: {'*' * len(pwd)}"),
    )

TextEditor
----------

Multi-line text editor.

.. code-block:: python

    editor = nib.TextEditor(
        text="Initial content\nMultiple lines",
        on_change=lambda text: print(f"Text changed: {len(text)} chars"),
    )

**Parameters:**

- ``text`` - Current text content
- ``on_change`` - Callback when text changes
- ``font`` - Font for the text
- ``foreground_color`` - Text color

Markdown
--------

Render Markdown content.

.. code-block:: python

    nib.Markdown(
        content="# Heading\n\nThis is **bold** and *italic*.\n\n- List item 1\n- List item 2",
    )

**Parameters:**

- ``content`` - Markdown string to render
- ``base_url`` - Base URL for relative links

Label
-----

Text with an icon (SF Symbol).

.. code-block:: python

    nib.Label("Downloads", system_image="arrow.down.circle.fill")

    # With custom styling
    nib.Label(
        "Favorites",
        system_image="star.fill",
        foreground_color=nib.Color.YELLOW,
    )

Link
----

Clickable URL link.

.. code-block:: python

    nib.Link(
        "Visit Website",
        destination="https://example.com",
    )

    # With icon
    nib.Link(
        destination="https://github.com/user/repo",
        label=nib.Label("GitHub", system_image="link"),
    )
