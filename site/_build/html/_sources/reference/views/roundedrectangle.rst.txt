RoundedRectangle
================

A rectangle with rounded corners.

.. code-block:: python

    nib.RoundedRectangle(corner_radius=12, fill="#333")

.. autoclass:: nib.RoundedRectangle
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``corner_radius`` - Radius of the corners
- ``fill`` - Fill color
- ``stroke`` - Stroke/border color
- ``stroke_width`` - Width of the stroke
- ``width``, ``height`` - Dimensions

Examples
--------

**Basic Rounded Rectangle**

.. code-block:: python

    nib.RoundedRectangle(corner_radius=8, fill=nib.Color.BLUE)

**Card Background**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Card Title", font=nib.Font.HEADLINE),
            nib.Text("Card content here"),
        ],
        spacing=8,
        padding=16,
        background=nib.RoundedRectangle(
            corner_radius=12,
            fill="#262626",
        ),
    )

**With Border**

.. code-block:: python

    nib.RoundedRectangle(
        corner_radius=10,
        fill="#1a1a1a",
        stroke="#444",
        stroke_width=1,
    )

**Button Background**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.RoundedRectangle(
                corner_radius=8,
                fill=nib.Color.BLUE,
            ),
            nib.Text("Click Me", foreground_color=nib.Color.WHITE),
        ],
        padding={"horizontal": 16, "vertical": 8},
    )

**Tag/Badge**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.RoundedRectangle(
                corner_radius=4,
                fill="#4CAF50",
            ),
            nib.Text(
                "NEW",
                font=nib.Font.CAPTION,
                foreground_color=nib.Color.WHITE,
            ),
        ],
        padding={"horizontal": 8, "vertical": 4},
    )

**Input Field Style**

.. code-block:: python

    nib.TextField(
        value="",
        placeholder="Search...",
        background=nib.RoundedRectangle(
            corner_radius=8,
            fill="#333",
            stroke="#555",
            stroke_width=1,
        ),
        padding=8,
    )
