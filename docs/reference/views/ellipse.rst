Ellipse
=======

An elliptical (oval) shape.

.. code-block:: python

    nib.Ellipse(fill=nib.Color.BLUE)

    nib.Ellipse(
        fill="#333",
        width=100,
        height=50,
    )

.. autoclass:: nib.Ellipse
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

**Basic Ellipse**

.. code-block:: python

    nib.Ellipse(fill=nib.Color.PURPLE)

**Wide Ellipse**

.. code-block:: python

    nib.Ellipse(
        fill=nib.Color.ORANGE,
        width=200,
        height=100,
    )

**Tall Ellipse**

.. code-block:: python

    nib.Ellipse(
        fill=nib.Color.TEAL,
        width=50,
        height=100,
    )

**With Stroke**

.. code-block:: python

    nib.Ellipse(
        fill="transparent",
        stroke=nib.Color.BLUE,
        stroke_width=2,
        width=100,
        height=60,
    )

**Decorative Element**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Ellipse(
                fill="#FF6B6B20",  # Semi-transparent
                width=200,
                height=100,
            ),
            nib.Text("Featured"),
        ],
    )
