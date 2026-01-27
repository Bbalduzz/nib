Font
====

Fonts control the typography of text elements.

Font Class
----------

.. autoclass:: nib.Font
   :members:
   :undoc-members:

System Fonts
------------

Use predefined system font styles:

.. code-block:: python

    nib.Font.LARGE_TITLE   # Large title text
    nib.Font.TITLE         # Title text
    nib.Font.TITLE2        # Secondary title
    nib.Font.TITLE3        # Tertiary title
    nib.Font.HEADLINE      # Headline text
    nib.Font.SUBHEADLINE   # Subheadline text
    nib.Font.BODY          # Body text (default)
    nib.Font.CALLOUT       # Callout text
    nib.Font.FOOTNOTE      # Footnote text
    nib.Font.CAPTION       # Caption text
    nib.Font.CAPTION2      # Secondary caption

Custom Fonts
------------

Create fonts with custom size and weight:

.. code-block:: python

    # System font with custom size
    nib.Font.system(size=18)

    # System font with size and weight
    nib.Font.system(size=24, weight=nib.FontWeight.BOLD)

    # Monospaced font
    nib.Font.monospaced(size=14)

FontWeight
----------

.. autoclass:: nib.FontWeight
   :members:
   :undoc-members:

Available weights:

.. code-block:: python

    nib.FontWeight.ULTRALIGHT
    nib.FontWeight.THIN
    nib.FontWeight.LIGHT
    nib.FontWeight.REGULAR
    nib.FontWeight.MEDIUM
    nib.FontWeight.SEMIBOLD
    nib.FontWeight.BOLD
    nib.FontWeight.HEAVY
    nib.FontWeight.BLACK

Examples
--------

**Heading Hierarchy**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Large Title", font=nib.Font.LARGE_TITLE),
            nib.Text("Title", font=nib.Font.TITLE),
            nib.Text("Headline", font=nib.Font.HEADLINE),
            nib.Text("Body text", font=nib.Font.BODY),
            nib.Text("Caption", font=nib.Font.CAPTION),
        ],
        spacing=8,
    )

**Custom Styled Text**

.. code-block:: python

    nib.Text(
        "Important",
        font=nib.Font.system(size=20, weight=nib.FontWeight.BOLD),
        foreground_color=nib.Color.RED,
    )

**Code Display**

.. code-block:: python

    nib.Text(
        "let x = 42",
        font=nib.Font.monospaced(size=14),
        foreground_color=nib.Color.GREEN,
    )

**Weight Only**

.. code-block:: python

    nib.Text(
        "Bold text",
        font_weight=nib.FontWeight.BOLD,
    )
