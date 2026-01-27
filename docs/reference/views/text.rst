Text
====

A view that displays one or more lines of read-only text.

.. code-block:: python

    nib.Text("Hello, World!")

    nib.Text(
        "Styled Text",
        font=nib.Font.TITLE,
        foreground_color=nib.Color.BLUE,
    )

.. autoclass:: nib.Text
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``content`` - The text string to display
- ``font`` - Font style (:class:`~nib.Font`)
- ``font_weight`` - Text weight (:class:`~nib.FontWeight`)
- ``foreground_color`` - Text color
- ``multiline_text_alignment`` - Alignment for multi-line text

Reactive Updates
----------------

Update the text content dynamically:

.. code-block:: python

    counter = nib.Text("0")

    def increment():
        counter.content = str(int(counter.content) + 1)

Examples
--------

**Basic Text**

.. code-block:: python

    nib.Text("Hello, World!")

**Styled Text**

.. code-block:: python

    nib.Text(
        "Title",
        font=nib.Font.LARGE_TITLE,
        font_weight=nib.FontWeight.BOLD,
    )

**Colored Text**

.. code-block:: python

    nib.Text(
        "Error message",
        foreground_color=nib.Color.RED,
    )

**Secondary Text**

.. code-block:: python

    nib.Text(
        "Subtitle",
        font=nib.Font.SUBHEADLINE,
        foreground_color=nib.Color.SECONDARY,
    )

**System Font with Custom Size**

.. code-block:: python

    nib.Text(
        "Custom Size",
        font=nib.Font.system(size=24, weight=nib.FontWeight.MEDIUM),
    )
