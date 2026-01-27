HStack
======

A horizontal stack that arranges its children in a left-to-right line.

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Left"),
            nib.Spacer(),
            nib.Text("Right"),
        ],
        spacing=8,
    )

.. autoclass:: nib.HStack
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views
- ``spacing`` - Space between children (default: 0)
- ``alignment`` - Vertical alignment of children (:class:`~nib.VerticalAlignment`)
- ``padding`` - Padding around the stack

Examples
--------

**Basic Row**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Label("Downloads", system_image="arrow.down.circle"),
            nib.Spacer(),
            nib.Text("5"),
        ],
    )

**Button Row**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Button("Cancel", action=cancel),
            nib.Spacer(),
            nib.Button("Save", action=save, style=nib.ButtonStyle.BORDEREDPROMINENT),
        ],
        spacing=8,
        padding=16,
    )

**Aligned to Top**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Title", font=nib.Font.TITLE),
            nib.Text("Subtitle", foreground_color=nib.Color.SECONDARY),
        ],
        alignment=nib.VerticalAlignment.TOP,
        spacing=8,
    )
