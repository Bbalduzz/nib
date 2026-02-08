Shapes
======

SwiftUI shape views for decorative elements and backgrounds.

Basic Shapes
------------

Rectangle
~~~~~~~~~

.. code-block:: python

    nib.Rectangle(
        fill="#3498db",
        stroke="#2980b9",
        stroke_width=2,
    )

    # As a background
    nib.VStack(
        controls=[nib.Text("Hello")],
        background=nib.Rectangle(fill="#1a1a1a"),
    )

Rounded Corners
~~~~~~~~~~~~~~~

Use ``corner_radius`` on ``Rectangle`` for rounded corners. Pass a ``float`` for uniform
corners, or a ``nib.CornerRadius`` for per-corner control.

.. code-block:: python

    nib.Rectangle(
        corner_radius=12,
        fill="#e74c3c",
    )

    # Per-corner control
    nib.Rectangle(
        corner_radius=nib.CornerRadius(
            top_left=20,
            top_right=20,
            bottom_left=0,
            bottom_right=0,
        ),
        fill="#9b59b6",
    )

Circle
~~~~~~

.. code-block:: python

    nib.Circle(
        fill="#2ecc71",
        stroke="#27ae60",
        stroke_width=3,
    )

Ellipse
~~~~~~~

.. code-block:: python

    nib.Ellipse(
        fill="#f39c12",
        width=100,
        height=50,
    )

Capsule
~~~~~~~

Pill-shaped rounded rectangle.

.. code-block:: python

    nib.Capsule(
        fill="#1abc9c",
        width=100,
        height=40,
    )

Gradients
---------

Use gradient views as fills for shapes or as standalone backgrounds.

LinearGradient
~~~~~~~~~~~~~~

.. code-block:: python

    nib.LinearGradient(
        colors=["#FF0000", "#0000FF"],
        start_point=nib.UnitPoint.TOP,
        end_point=nib.UnitPoint.BOTTOM,
    )

    # As shape fill
    nib.Rectangle(
        fill=nib.LinearGradient(
            colors=["#667eea", "#764ba2"],
            start_point=nib.UnitPoint.TOP_LEADING,
            end_point=nib.UnitPoint.BOTTOM_TRAILING,
        ),
    )

RadialGradient
~~~~~~~~~~~~~~

.. code-block:: python

    nib.RadialGradient(
        colors=["#FFFFFF", "#000000"],
        center=nib.UnitPoint.CENTER,
        start_radius=0,
        end_radius=100,
    )

AngularGradient
~~~~~~~~~~~~~~~

.. code-block:: python

    nib.AngularGradient(
        colors=["#FF0000", "#00FF00", "#0000FF", "#FF0000"],
        center=nib.UnitPoint.CENTER,
    )

EllipticalGradient
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    nib.EllipticalGradient(
        colors=["#FFFFFF", "#000000"],
        center=nib.UnitPoint.CENTER,
    )

**UnitPoint Values:**

.. code-block:: python

    nib.UnitPoint.TOP_LEADING
    nib.UnitPoint.TOP
    nib.UnitPoint.TOP_TRAILING
    nib.UnitPoint.LEADING
    nib.UnitPoint.CENTER
    nib.UnitPoint.TRAILING
    nib.UnitPoint.BOTTOM_LEADING
    nib.UnitPoint.BOTTOM
    nib.UnitPoint.BOTTOM_TRAILING

Using Shapes
------------

As Backgrounds
~~~~~~~~~~~~~~

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Card Title", font=nib.Font.HEADLINE),
            nib.Text("Card content goes here"),
        ],
        padding=16,
        background=nib.Rectangle(
            corner_radius=12,
            fill="#262626",
            stroke="#383838",
            stroke_width=1,
        ),
    )

As Overlays
~~~~~~~~~~~

.. code-block:: python

    nib.Image(
        name="avatar.png",
        width=50,
        height=50,
        overlay=nib.Circle(
            stroke="#00FF00",
            stroke_width=3,
        ),
    )

As Clip Shapes
~~~~~~~~~~~~~~

.. code-block:: python

    nib.Image(
        name="photo.jpg",
        clip_shape="circle",  # Shorthand for circular clip
    )

    # Or with explicit shape
    nib.Image(
        name="photo.jpg",
        clip_shape=nib.Rectangle(corner_radius=12),
    )

Combining Shapes
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Card with gradient background and border
    nib.ZStack(controls=[
        nib.Rectangle(
            corner_radius=16,
            fill=nib.LinearGradient(
                colors=["#1a1a2e", "#16213e"],
                start_point=nib.UnitPoint.TOP,
                end_point=nib.UnitPoint.BOTTOM,
            ),
        ),
        nib.Rectangle(
            corner_radius=16,
            stroke="#0f3460",
            stroke_width=1,
        ),
        nib.VStack(
            controls=[nib.Text("Content")],
            padding=20,
        ),
    ])
