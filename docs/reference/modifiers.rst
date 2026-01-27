Modifiers
=========

All Nib views support a common set of modifier parameters for styling.
Pass these as constructor arguments to any view.

Layout Modifiers
----------------

**Size**

.. code-block:: python

    nib.Rectangle(
        width=100,           # Fixed width
        height=50,           # Fixed height
        min_width=50,        # Minimum width
        min_height=30,       # Minimum height
        max_width=200,       # Maximum width
        max_height="infinity",  # Expand to fill
    )

**Padding**

.. code-block:: python

    # Uniform padding
    nib.VStack(controls=[...], padding=16)

    # Per-side padding
    nib.VStack(
        controls=[...],
        padding={
            "top": 8,
            "bottom": 8,
            "leading": 16,
            "trailing": 16,
        },
    )

    # Horizontal/vertical shorthand
    nib.VStack(
        controls=[...],
        padding={"horizontal": 16, "vertical": 8},
    )

Appearance Modifiers
--------------------

**Background**

.. code-block:: python

    # Color background
    nib.VStack(controls=[...], background="#333")
    nib.VStack(controls=[...], background=nib.Color.BLUE)

    # View background
    nib.VStack(
        controls=[...],
        background=nib.RoundedRectangle(
            corner_radius=12,
            fill="#262626",
            stroke="#383838",
        ),
    )

**Foreground Color**

.. code-block:: python

    nib.Text("Hello", foreground_color=nib.Color.BLUE)
    nib.Label("Icon", system_image="star", foreground_color="#FF6600")

**Opacity**

.. code-block:: python

    nib.Rectangle(fill=nib.Color.RED, opacity=0.5)

**Corner Radius**

.. code-block:: python

    nib.VStack(
        controls=[...],
        corner_radius=12,
        background="#333",
    )

Shape Modifiers
---------------

**Fill and Stroke**

.. code-block:: python

    nib.Rectangle(
        fill="#333",
        stroke=nib.Color.WHITE,
        stroke_width=2,
    )

**Clip Shape**

.. code-block:: python

    # Clip to circle
    nib.Image(path="/path/to/image.jpg", clip_shape="circle")

    # Clip to capsule
    nib.Image(path="/path/to/image.jpg", clip_shape="capsule")

    # Clip to custom shape
    nib.Image(
        path="/path/to/image.jpg",
        clip_shape=nib.RoundedRectangle(corner_radius=20),
    )

Shadow & Border
---------------

**Shadow**

.. code-block:: python

    nib.VStack(
        controls=[...],
        shadow_radius=10,
        shadow_color="#00000040",
        shadow_x=0,
        shadow_y=4,
    )

**Border**

.. code-block:: python

    nib.VStack(
        controls=[...],
        border_color="#444",
        border_width=1,
    )

Typography Modifiers
--------------------

**Font**

.. code-block:: python

    nib.Text("Title", font=nib.Font.TITLE)
    nib.Text("Custom", font=nib.Font.system(size=20, weight=nib.FontWeight.BOLD))

**Font Weight**

.. code-block:: python

    nib.Text("Bold", font_weight=nib.FontWeight.BOLD)

Animation Modifiers
-------------------

**Animation**

.. code-block:: python

    nib.Text(
        "Animated",
        animation=nib.Animation.spring(),
    )

**Content Transition**

.. code-block:: python

    nib.Text(
        counter_value,
        content_transition=nib.ContentTransition.NUMERICTEXT,
    )

**View Transition**

.. code-block:: python

    nib.VStack(
        controls=[...],
        transition=nib.Transition.SLIDE,
    )

Transform Modifiers
-------------------

**Scale**

.. code-block:: python

    nib.Label("Big", system_image="star", scale=1.5)
    nib.Label("Small", system_image="star", scale=0.5)

**Blend Mode**

.. code-block:: python

    nib.Rectangle(
        fill=nib.Color.RED,
        blend_mode=nib.BlendMode.MULTIPLY,
    )

Overlay
-------

**Overlay View**

.. code-block:: python

    nib.Image(
        path="/path/to/image.jpg",
        overlay=nib.Circle(
            stroke=nib.Color.WHITE,
            stroke_width=2,
        ),
    )

Drag and Drop
-------------

**On Drop**

.. code-block:: python

    def handle_drop(files: list[str]):
        print(f"Dropped: {files}")

    nib.VStack(
        controls=[nib.Text("Drop files here")],
        on_drop=handle_drop,
    )
