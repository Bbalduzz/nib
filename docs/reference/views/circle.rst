Circle
======

A circular shape.

.. code-block:: python

    nib.Circle(fill=nib.Color.BLUE)

    nib.Circle(
        fill="#333",
        stroke=nib.Color.WHITE,
        stroke_width=2,
        width=50,
        height=50,
    )

.. autoclass:: nib.Circle
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``fill`` - Fill color
- ``stroke`` - Stroke/border color
- ``stroke_width`` - Width of the stroke
- ``width``, ``height`` - Dimensions (circle uses the smaller value)

Examples
--------

**Basic Circle**

.. code-block:: python

    nib.Circle(fill=nib.Color.RED)

**With Stroke**

.. code-block:: python

    nib.Circle(
        fill="transparent",
        stroke=nib.Color.BLUE,
        stroke_width=2,
    )

**Fixed Size**

.. code-block:: python

    nib.Circle(
        fill=nib.Color.GREEN,
        width=64,
        height=64,
    )

**Avatar Placeholder**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Circle(fill="#4A90D9"),
            nib.Text(
                "JD",
                font=nib.Font.TITLE,
                foreground_color=nib.Color.WHITE,
            ),
        ],
        width=64,
        height=64,
    )

**Status Indicator**

.. code-block:: python

    # Online indicator
    nib.Circle(fill="#4CAF50", width=12, height=12)

    # Offline indicator
    nib.Circle(fill="#9E9E9E", width=12, height=12)

    # Busy indicator
    nib.Circle(fill="#F44336", width=12, height=12)

**Progress Ring**

.. code-block:: python

    nib.Circle(
        stroke=nib.Color.BLUE,
        stroke_width=4,
        width=50,
        height=50,
    )

**Color Palette**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Circle(fill=color, width=24, height=24)
            for color in ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        ],
        spacing=8,
    )
