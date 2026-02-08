ZStack
======

An overlay stack that layers its children on top of each other.

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Circle(fill=nib.Color.BLUE),
            nib.Text("Hello"),
        ],
    )

.. autoclass:: nib.ZStack
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views (first is bottom, last is top)
- ``alignment`` - Alignment of children within the stack (:class:`~nib.Alignment`)
- ``padding`` - Padding around the stack

Examples
--------

**Overlaid Text on Shape**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.RoundedRectangle(corner_radius=8, fill="#333"),
            nib.Text("Badge", foreground_color=nib.Color.WHITE),
        ],
        alignment=nib.Alignment.CENTER,
    )

**Profile Avatar with Badge**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Circle(fill=nib.Color.BLUE, width=50, height=50),
            nib.Text("JD", foreground_color=nib.Color.WHITE),
        ],
        alignment=nib.Alignment.CENTER,
    )

**Image with Gradient Overlay**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Image(path="/path/to/image.jpg"),
            nib.Rectangle(fill="#00000080"),  # Semi-transparent overlay
            nib.Text("Caption", foreground_color=nib.Color.WHITE),
        ],
        alignment=nib.Alignment.BOTTOM,
    )
