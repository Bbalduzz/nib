VisualEffectBlur
================

A view that applies a blur effect, creating a frosted glass appearance similar
to the macOS menu bar and system UI.

.. code-block:: python

    import nib

    blur = nib.VisualEffectBlur(
        material=nib.BlurStyle.POPOVER,
        corner_radius=10,
    )

Parameters
----------

material : BlurStyle, optional
    The blur material style (default: POPOVER).

blending_mode : BlurBlendingMode, optional
    How the blur blends with content (default: BEHIND_WINDOW).

is_emphasized : bool, optional
    Whether to use emphasized appearance (default: False).

corner_radius : float, optional
    Corner radius for rounded blur edges.

Blur Styles
-----------

.. code-block:: python

    # Standard materials
    nib.BlurStyle.POPOVER           # Popover background
    nib.BlurStyle.MENU              # Menu background
    nib.BlurStyle.SIDEBAR           # Sidebar style
    nib.BlurStyle.SHEET             # Sheet background
    nib.BlurStyle.HUD               # HUD style
    nib.BlurStyle.WINDOW_BACKGROUND
    nib.BlurStyle.CONTENT_BACKGROUND
    nib.BlurStyle.HEADER_VIEW
    nib.BlurStyle.FULLSCREEN_UI
    nib.BlurStyle.TITLEBAR
    nib.BlurStyle.SELECTION
    nib.BlurStyle.UNDER_WINDOW_BACKGROUND
    nib.BlurStyle.UNDER_PAGE_BACKGROUND

    # Vibrancy levels
    nib.BlurStyle.ULTRA_THIN
    nib.BlurStyle.THIN
    nib.BlurStyle.REGULAR
    nib.BlurStyle.THICK
    nib.BlurStyle.ULTRA_THICK

Blending Modes
--------------

.. code-block:: python

    nib.BlurBlendingMode.BEHIND_WINDOW  # Blur content behind the window
    nib.BlurBlendingMode.WITHIN_WINDOW  # Blur content within the window

As Background
-------------

The most common use is as a background for other views:

.. code-block:: python

    card = nib.VStack(
        controls=[
            nib.Text("Card Title", font=nib.Font.headline),
            nib.Text("Card content goes here"),
        ],
        spacing=8,
        padding=16,
        background=nib.VisualEffectBlur(
            material=nib.BlurStyle.POPOVER,
            corner_radius=12,
        ),
    )

Example: Frosted Card
---------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "Blur Demo"
        app.width = 300
        app.height = 200

        app.build(
            nib.VStack(
                controls=[
                    nib.Text("Frosted Glass Effect"),
                    nib.HStack(
                        controls=[
                            nib.SFSymbol("sparkles"),
                            nib.Text("Beautiful blur!"),
                        ],
                        spacing=8,
                        padding=16,
                        background=nib.VisualEffectBlur(
                            material=nib.BlurStyle.POPOVER,
                            corner_radius=10,
                        ),
                    ),
                ],
                spacing=16,
                padding=16,
            )
        )

    nib.run(main)

Example: Sidebar Style
----------------------

.. code-block:: python

    sidebar = nib.VStack(
        controls=[
            nib.Text("Navigation", font=nib.Font.headline),
            nib.Button("Home", action=go_home),
            nib.Button("Settings", action=go_settings),
        ],
        spacing=8,
        padding=12,
        background=nib.VisualEffectBlur(
            material=nib.BlurStyle.SIDEBAR,
            blending_mode=nib.BlurBlendingMode.BEHIND_WINDOW,
        ),
    )

.. note::

    VisualEffectBlur wraps ``NSVisualEffectView`` on macOS. The exact appearance
    depends on the system theme (light/dark mode) and the content behind the view.
