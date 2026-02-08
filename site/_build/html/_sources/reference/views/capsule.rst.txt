Capsule
=======

A pill-shaped view with fully rounded ends.

.. code-block:: python

    nib.Capsule(fill=nib.Color.BLUE)

    nib.Capsule(
        fill="#333",
        width=100,
        height=40,
    )

.. autoclass:: nib.Capsule
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

**Basic Capsule**

.. code-block:: python

    nib.Capsule(fill=nib.Color.BLUE)

**Pill Button Background**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Capsule(fill=nib.Color.BLUE),
            nib.Text("Subscribe", foreground_color=nib.Color.WHITE),
        ],
        padding={"horizontal": 20, "vertical": 10},
    )

**Tag/Chip**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Capsule(fill="#E3F2FD"),
            nib.Text("Python", foreground_color="#1976D2"),
        ],
        padding={"horizontal": 12, "vertical": 6},
    )

**With Stroke**

.. code-block:: python

    nib.Capsule(
        fill="transparent",
        stroke=nib.Color.BLUE,
        stroke_width=1,
        width=80,
        height=30,
    )

**Category Tags**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.ZStack(
                controls=[
                    nib.Capsule(fill="#FFE0B2"),
                    nib.Text("Design", font=nib.Font.CAPTION),
                ],
                padding={"horizontal": 10, "vertical": 4},
            ),
            nib.ZStack(
                controls=[
                    nib.Capsule(fill="#C8E6C9"),
                    nib.Text("Code", font=nib.Font.CAPTION),
                ],
                padding={"horizontal": 10, "vertical": 4},
            ),
        ],
        spacing=8,
    )

**Progress Indicator Track**

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Capsule(fill="#333", width=200, height=8),
            nib.Capsule(fill=nib.Color.BLUE, width=120, height=8),
        ],
        alignment=nib.Alignment.LEADING,
    )
