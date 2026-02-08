Types & Styling
===============

Core types for colors, fonts, animations, and enums.

Color
-----

Colors can be specified as hex strings or ``Color`` objects.

.. code-block:: python

    # Hex strings
    nib.Text("Red", foreground_color="#FF0000")
    nib.Text("Blue", foreground_color="#0000FF")
    nib.Text("With alpha", foreground_color="#FF000080")  # 50% opacity

    # Color constants
    nib.Text("Red", foreground_color=nib.Color.RED)
    nib.Text("Blue", foreground_color=nib.Color.BLUE)

    # Custom color
    nib.Color(hex="#FF5733")
    nib.Color(red=1.0, green=0.34, blue=0.2, alpha=1.0)

**Color Constants:**

.. code-block:: python

    nib.Color.BLACK
    nib.Color.WHITE
    nib.Color.GRAY
    nib.Color.RED
    nib.Color.GREEN
    nib.Color.BLUE
    nib.Color.ORANGE
    nib.Color.YELLOW
    nib.Color.PINK
    nib.Color.PURPLE
    nib.Color.TEAL
    nib.Color.INDIGO
    nib.Color.BROWN
    nib.Color.MINT
    nib.Color.CYAN
    nib.Color.CLEAR       # Transparent
    nib.Color.PRIMARY     # System accent
    nib.Color.SECONDARY

Font
----

Text styling with system or custom fonts.

.. code-block:: python

    # Preset fonts
    nib.Text("Title", font=nib.Font.TITLE)
    nib.Text("Body", font=nib.Font.BODY)
    nib.Text("Caption", font=nib.Font.CAPTION)

    # Custom system font
    nib.Text("Custom", font=nib.Font.system(size=18, weight=nib.FontWeight.BOLD))

    # Custom named font
    nib.Text("Mono", font=nib.Font.custom("SF Mono", size=14))

**Font Presets:**

.. code-block:: python

    nib.Font.LARGE_TITLE    # 34pt
    nib.Font.TITLE          # 28pt
    nib.Font.TITLE2         # 22pt
    nib.Font.TITLE3         # 20pt
    nib.Font.HEADLINE       # 17pt semibold
    nib.Font.BODY           # 17pt
    nib.Font.CALLOUT        # 16pt
    nib.Font.SUBHEADLINE    # 15pt
    nib.Font.FOOTNOTE       # 13pt
    nib.Font.CAPTION        # 12pt
    nib.Font.CAPTION2       # 11pt

**Font Weights:**

.. code-block:: python

    nib.FontWeight.ULTRALIGHT
    nib.FontWeight.THIN
    nib.FontWeight.LIGHT
    nib.FontWeight.REGULAR
    nib.FontWeight.MEDIUM
    nib.FontWeight.SEMIBOLD
    nib.FontWeight.BOLD
    nib.FontWeight.HEAVY
    nib.FontWeight.BLACK

Animation
---------

Animate view transitions.

.. code-block:: python

    # Animated button
    nib.Button(
        "Click Me",
        action=on_click,
        animation=nib.Animation.spring(),
    )

    # Animated view changes
    nib.Text(
        "Animated",
        animation=nib.Animation.ease_in_out(duration=0.3),
    )

**Animation Types:**

.. code-block:: python

    # Spring animations
    nib.Animation.spring()
    nib.Animation.spring(response=0.5, damping=0.7, blend_duration=0)
    nib.Animation.interactiveSpring()
    nib.Animation.bouncy()
    nib.Animation.snappy()
    nib.Animation.smooth()

    # Timing animations
    nib.Animation.linear(duration=0.3)
    nib.Animation.ease_in(duration=0.3)
    nib.Animation.ease_out(duration=0.3)
    nib.Animation.ease_in_out(duration=0.3)

    # No animation
    nib.Animation.none()

Transitions
~~~~~~~~~~~

Animate view appearance:

.. code-block:: python

    nib.Text(
        "Fade In",
        transition=nib.Transition.opacity,
    )

    nib.Text(
        "Slide",
        transition=nib.Transition.slide,
    )

    # Combined transitions
    nib.Text(
        "Combined",
        transition=nib.Transition.combined([
            nib.Transition.opacity,
            nib.Transition.scale,
        ]),
    )

Alignment
---------

.. code-block:: python

    # Horizontal alignment (for VStack)
    nib.HorizontalAlignment.LEADING
    nib.HorizontalAlignment.CENTER
    nib.HorizontalAlignment.TRAILING

    # Vertical alignment (for HStack)
    nib.VerticalAlignment.TOP
    nib.VerticalAlignment.CENTER
    nib.VerticalAlignment.BOTTOM
    nib.VerticalAlignment.FIRST_TEXT_BASELINE
    nib.VerticalAlignment.LAST_TEXT_BASELINE

    # 2D alignment (for ZStack)
    nib.Alignment.TOP_LEADING
    nib.Alignment.TOP
    nib.Alignment.TOP_TRAILING
    nib.Alignment.LEADING
    nib.Alignment.CENTER
    nib.Alignment.TRAILING
    nib.Alignment.BOTTOM_LEADING
    nib.Alignment.BOTTOM
    nib.Alignment.BOTTOM_TRAILING

Control Enums
-------------

.. code-block:: python

    # Button styles
    nib.ButtonStyle.AUTOMATIC
    nib.ButtonStyle.BORDERED
    nib.ButtonStyle.BORDEREDPROMINENT
    nib.ButtonStyle.BORDERLESS
    nib.ButtonStyle.PLAIN
    nib.ButtonStyle.LINK

    # Button roles
    nib.ButtonRole.DESTRUCTIVE
    nib.ButtonRole.CANCEL

    # Control sizes
    nib.ControlSize.MINI
    nib.ControlSize.SMALL
    nib.ControlSize.REGULAR
    nib.ControlSize.LARGE
    nib.ControlSize.EXTRA_LARGE

    # Picker styles
    nib.PickerStyle.AUTOMATIC
    nib.PickerStyle.INLINE
    nib.PickerStyle.MENU
    nib.PickerStyle.SEGMENTED
    nib.PickerStyle.WHEEL

    # List styles
    nib.ListStyle.AUTOMATIC
    nib.ListStyle.INSET
    nib.ListStyle.INSET_GROUPED
    nib.ListStyle.PLAIN
    nib.ListStyle.SIDEBAR

    # Text field styles
    nib.TextFieldStyle.PLAIN
    nib.TextFieldStyle.ROUNDED_BORDER
    nib.TextFieldStyle.SQUAREBORDER

Blend Modes
-----------

For Canvas drawing and compositing:

.. code-block:: python

    nib.BlendMode.NORMAL
    nib.BlendMode.MULTIPLY
    nib.BlendMode.SCREEN
    nib.BlendMode.OVERLAY
    nib.BlendMode.DARKEN
    nib.BlendMode.LIGHTEN
    nib.BlendMode.COLOR_DODGE
    nib.BlendMode.COLOR_BURN
    nib.BlendMode.SOFT_LIGHT
    nib.BlendMode.HARD_LIGHT
    nib.BlendMode.DIFFERENCE
    nib.BlendMode.EXCLUSION
    nib.BlendMode.HUE
    nib.BlendMode.SATURATION
    nib.BlendMode.COLOR
    nib.BlendMode.LUMINOSITY
