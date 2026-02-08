Color
=====

Colors can be specified as hex strings, system color names, or ``Color`` constants.

Color Class
-----------

.. autoclass:: nib.Color
   :members:
   :undoc-members:

Usage
-----

**Hex Colors**

.. code-block:: python

    # 6-digit hex
    nib.Text("Red", foreground_color="#FF0000")

    # 8-digit hex with alpha
    nib.Rectangle(fill="#FF000080")  # 50% transparent red

    # 3-digit shorthand
    nib.Circle(fill="#F00")

**System Colors**

.. code-block:: python

    nib.Text("Primary", foreground_color=nib.Color.PRIMARY)
    nib.Text("Secondary", foreground_color=nib.Color.SECONDARY)
    nib.Rectangle(fill=nib.Color.BLUE)

**Semantic Colors**

These colors adapt to light/dark mode automatically:

.. code-block:: python

    nib.Color.PRIMARY      # Primary text color
    nib.Color.SECONDARY    # Secondary/muted text
    nib.Color.TERTIARY     # Tertiary text
    nib.Color.QUATERNARY   # Quaternary text

**Standard Colors**

.. code-block:: python

    nib.Color.RED
    nib.Color.ORANGE
    nib.Color.YELLOW
    nib.Color.GREEN
    nib.Color.MINT
    nib.Color.TEAL
    nib.Color.CYAN
    nib.Color.BLUE
    nib.Color.INDIGO
    nib.Color.PURPLE
    nib.Color.PINK
    nib.Color.BROWN
    nib.Color.WHITE
    nib.Color.GRAY
    nib.Color.BLACK
    nib.Color.CLEAR  # Transparent

Examples
--------

**Text Colors**

.. code-block:: python

    nib.Text("Error", foreground_color=nib.Color.RED)
    nib.Text("Success", foreground_color=nib.Color.GREEN)
    nib.Text("Warning", foreground_color=nib.Color.ORANGE)

**Backgrounds**

.. code-block:: python

    nib.VStack(
        controls=[...],
        background="#1a1a1a",
    )

    nib.VStack(
        controls=[...],
        background=nib.RoundedRectangle(
            corner_radius=8,
            fill="#262626",
            stroke="#383838",
        ),
    )

**Gradients (via shapes)**

.. code-block:: python

    # Use overlapping shapes with opacity for gradient effects
    nib.ZStack(
        controls=[
            nib.Rectangle(fill="#0000FF", opacity=0.8),
            nib.Rectangle(fill="#FF0000", opacity=0.3),
        ],
    )
