Canvas & Drawing
================

The Canvas view provides a Core Graphics drawing surface for custom graphics,
images, and interactive drawing.

Canvas Basics
-------------

Create a canvas and draw shapes:

.. code-block:: python

    import nib

    canvas = nib.Canvas(width=400, height=300)
    canvas.draw([
        nib.draw.Rect(x=10, y=10, width=100, height=50, fill="#3498db"),
        nib.draw.Circle(cx=200, cy=100, radius=40, fill="#e74c3c"),
        nib.draw.Text("Hello!", x=10, y=250, fill="#ffffff"),
    ])

    app.build(canvas)

Canvas Methods
--------------

.. code-block:: python

    # Replace all commands
    canvas.draw([...])

    # Add single command
    canvas.append(nib.draw.Circle(cx=50, cy=50, radius=10, fill="#FF0000"))

    # Clear canvas
    canvas.clear()

**Canvas Parameters:**

- ``width``, ``height`` - Canvas dimensions
- ``background_color`` - Background fill (hex string or None for transparent)
- ``enable_gestures`` - Enable pan/hover gesture tracking

Drawing Primitives
------------------

All primitives are in the ``nib.draw`` module.

Rect
~~~~

.. code-block:: python

    nib.draw.Rect(
        x=10, y=10,
        width=100, height=50,
        corner_radius=8,       # Rounded corners
        fill="#3498db",        # Fill color or gradient
        stroke="#2980b9",      # Stroke color
        stroke_width=2,
        opacity=0.9,
    )

Circle
~~~~~~

.. code-block:: python

    nib.draw.Circle(
        cx=100, cy=100,        # Center coordinates
        radius=40,
        fill="#e74c3c",
        stroke="#c0392b",
        stroke_width=2,
    )

Ellipse
~~~~~~~

.. code-block:: python

    nib.draw.Ellipse(
        cx=150, cy=100,
        rx=60, ry=30,          # Horizontal/vertical radii
        fill="#9b59b6",
    )

Line
~~~~

.. code-block:: python

    nib.draw.Line(
        x1=0, y1=0,
        x2=200, y2=200,
        stroke="#2ecc71",
        stroke_width=3,
        line_cap="round",      # "butt", "round", "square"
    )

Arc
~~~

.. code-block:: python

    import math

    nib.draw.Arc(
        cx=100, cy=100,
        radius=50,
        start_angle=0,
        end_angle=math.pi,     # Radians
        clockwise=True,
        fill="#f39c12",
        stroke="#e67e22",
    )

Path
~~~~

Simple polygon from points:

.. code-block:: python

    nib.draw.Path(
        points=[(50, 10), (90, 90), (10, 90)],  # Triangle
        closed=True,
        fill="#1abc9c",
        stroke="#16a085",
    )

    # Convenience wrapper for closed polygons
    nib.draw.Polygon(
        points=[(50, 10), (90, 90), (10, 90)],
        fill="#1abc9c",
    )

BezierPath
~~~~~~~~~~

Complex paths with curves using typed path elements:

.. code-block:: python

    from nib.draw import BezierPath, MoveTo, LineTo, CubicTo, QuadraticTo, Close

    nib.draw.BezierPath(
        elements=[
            MoveTo(25, 125),
            QuadraticTo(cp1x=50, cp1y=25, x=135, y=35),
            CubicTo(cp1x=150, cp1y=150, cp2x=200, cp2y=50, x=250, y=100),
            LineTo(250, 200),
            Close(),
        ],
        fill="#F06292",
        stroke="#E91E63",
        stroke_width=2,
    )

**Path Elements:**

- ``MoveTo(x, y)`` - Move to point
- ``LineTo(x, y)`` - Line to point
- ``QuadraticTo(cp1x, cp1y, x, y, w=1.0)`` - Quadratic bezier curve
- ``CubicTo(cp1x, cp1y, cp2x, cp2y, x, y)`` - Cubic bezier curve
- ``ArcTo(x, y, radius, rotation, large_arc, sweep)`` - Arc to point
- ``Close()`` - Close path

Text
~~~~

.. code-block:: python

    nib.draw.Text(
        "Hello Canvas!",
        x=10, y=50,
        fill="#ffffff",
        font_size=24,
        font_weight="bold",    # "regular", "bold", "light", etc.
        font_name="SF Pro",    # System font name
    )

Image
~~~~~

Draw images from bytes:

.. code-block:: python

    # From file
    with open("photo.jpg", "rb") as f:
        image_data = f.read()

    nib.draw.Image(
        data=image_data,
        x=0, y=0,
        width=200,
        height=150,
        opacity=0.9,
    )

    # For webcam/video frames, encode as JPEG
    import cv2
    ret, frame = cap.read()
    _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    canvas.draw([nib.draw.Image(data=jpeg.tobytes(), x=0, y=0)])

Points
~~~~~~

Draw multiple points or connected lines:

.. code-block:: python

    nib.draw.Points(
        points=[(10, 10), (50, 50), (100, 30)],
        point_mode=nib.draw.PointMode.POINTS,  # POINTS, LINES, POLYGON
        stroke="#FF0000",
        stroke_width=5,
        stroke_cap="round",
    )

Gradients
---------

Use gradients as fill values:

.. code-block:: python

    # Linear gradient
    nib.draw.Rect(
        x=10, y=10, width=100, height=100,
        fill=nib.draw.LinearGradient(
            start=(10, 10),
            end=(110, 110),
            colors=["#FF0000", "#0000FF"],
        ),
    )

    # Radial gradient
    nib.draw.Circle(
        cx=200, cy=100, radius=50,
        fill=nib.draw.RadialGradient(
            center=(200, 100),
            radius=50,
            colors=["#FFFF00", "#FF0000"],
        ),
    )

    # Sweep (angular) gradient
    nib.draw.Circle(
        cx=100, cy=100, radius=50,
        fill=nib.draw.SweepGradient(
            center=(100, 100),
            colors=["#FF0000", "#00FF00", "#0000FF", "#FF0000"],
        ),
    )

Gesture Handling
----------------

Enable interactive drawing:

.. code-block:: python

    canvas = nib.Canvas(width=400, height=300, enable_gestures=True)

    last_pos = None

    def on_pan_start(e):
        global last_pos
        last_pos = (e.x, e.y)

    def on_pan_update(e):
        global last_pos
        canvas.append(nib.draw.Line(
            x1=last_pos[0], y1=last_pos[1],
            x2=e.x, y2=e.y,
            stroke="#000000",
            stroke_width=3,
        ))
        last_pos = (e.x, e.y)

    canvas.on_pan_start = on_pan_start
    canvas.on_pan_update = on_pan_update

**Gesture Callbacks:**

- ``on_pan_start(e)`` - Mouse/pen pressed
- ``on_pan_update(e)`` - Dragging
- ``on_pan_end(e)`` - Released
- ``on_hover(e)`` - Mouse moved (not pressed)

Each callback receives a ``PanEvent`` with ``x`` and ``y`` coordinates.

Blend Modes
-----------

Apply blend modes to shapes:

.. code-block:: python

    nib.draw.Rect(
        x=50, y=50, width=100, height=100,
        fill="#FF0000",
        blend_mode=nib.BlendMode.MULTIPLY,
    )

**Available Blend Modes:**

``NORMAL``, ``MULTIPLY``, ``SCREEN``, ``OVERLAY``, ``DARKEN``, ``LIGHTEN``,
``COLOR_DODGE``, ``COLOR_BURN``, ``SOFT_LIGHT``, ``HARD_LIGHT``, ``DIFFERENCE``,
``EXCLUSION``, ``HUE``, ``SATURATION``, ``COLOR``, ``LUMINOSITY``,
``SOURCE_ATOP``, ``DESTINATION_OVER``, ``DESTINATION_OUT``, ``PLUS_LIGHTER``,
``PLUS_DARKER``

Utility Commands
----------------

Fill
~~~~

Fill the entire canvas:

.. code-block:: python

    nib.draw.Fill(fill="#1a1a1a")

    # With gradient
    nib.draw.Fill(
        fill=nib.draw.LinearGradient(
            start=(0, 0), end=(400, 300),
            colors=["#1a1a1a", "#2d2d2d"],
        )
    )

Shadow
~~~~~~

Material design shadows:

.. code-block:: python

    nib.draw.Shadow(
        path=[(10, 10), (110, 10), (110, 110), (10, 110)],
        elevation=10,
        color="#000000",
        opacity=0.3,
    )

Example: Drawing App
--------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "Draw"
        app.width = 400
        app.height = 350

        canvas = nib.Canvas(width=380, height=280, enable_gestures=True)
        canvas.draw([nib.draw.Fill(fill="#FFFFFF")])

        last_pos = None
        current_color = "#000000"

        def on_pan_start(e):
            nonlocal last_pos
            last_pos = (e.x, e.y)

        def on_pan_update(e):
            nonlocal last_pos
            canvas.append(nib.draw.Line(
                x1=last_pos[0], y1=last_pos[1],
                x2=e.x, y2=e.y,
                stroke=current_color,
                stroke_width=3,
                line_cap="round",
            ))
            last_pos = (e.x, e.y)

        canvas.on_pan_start = on_pan_start
        canvas.on_pan_update = on_pan_update

        def clear():
            canvas.draw([nib.draw.Fill(fill="#FFFFFF")])

        app.build(
            nib.VStack(
                controls=[
                    canvas,
                    nib.HStack(
                        controls=[
                            nib.Button("Clear", action=clear),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=8,
                padding=10,
            )
        )

    nib.run(main)
