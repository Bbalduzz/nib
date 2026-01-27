VStack
======

A vertical stack that arranges its children in a top-to-bottom line.

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("First"),
            nib.Text("Second"),
            nib.Text("Third"),
        ],
        spacing=8,
        padding=16,
    )

.. autoclass:: nib.VStack
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views
- ``spacing`` - Space between children (default: 0)
- ``alignment`` - Horizontal alignment of children (:class:`~nib.HorizontalAlignment`)
- ``padding`` - Padding around the stack

Examples
--------

**Basic Stack**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Hello"),
            nib.Text("World"),
        ],
    )

**With Spacing and Alignment**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Left aligned"),
            nib.Text("Also left"),
        ],
        spacing=12,
        alignment=nib.HorizontalAlignment.LEADING,
    )

**With Background**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Card Title", font=nib.Font.HEADLINE),
            nib.Text("Card content goes here"),
        ],
        spacing=8,
        padding=16,
        background=nib.RoundedRectangle(
            corner_radius=12,
            fill="#1a1a1a",
        ),
    )
