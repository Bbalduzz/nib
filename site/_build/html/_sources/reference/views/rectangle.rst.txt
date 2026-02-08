Rectangle
=========

A rectangular shape.

.. code-block:: python

    nib.Rectangle(fill=nib.Color.BLUE)

    nib.Rectangle(
        fill="#333",
        stroke=nib.Color.WHITE,
        stroke_width=2,
        width=100,
        height=50,
    )

.. autoclass:: nib.Rectangle
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``fill`` - Fill color
- ``stroke`` - Stroke/border color
- ``stroke_width`` - Width of the stroke
- ``width``, ``height`` - Dimensions

Examples
--------

**Basic Rectangle**

.. code-block:: python

    nib.Rectangle(fill=nib.Color.RED)

**With Stroke**

.. code-block:: python

    nib.Rectangle(
        fill="#1a1a1a",
        stroke="#444",
        stroke_width=1,
    )

**Fixed Size**

.. code-block:: python

    nib.Rectangle(
        fill=nib.Color.BLUE,
        width=200,
        height=100,
    )

**As Divider Line**

.. code-block:: python

    nib.Rectangle(
        fill="#333",
        height=1,
        max_width="infinity",
    )

**Color Swatch**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Rectangle(fill="#FF0000", width=30, height=30),
            nib.Rectangle(fill="#00FF00", width=30, height=30),
            nib.Rectangle(fill="#0000FF", width=30, height=30),
        ],
        spacing=8,
    )
