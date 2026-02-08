Effects
=======

Visual effects for views.

VisualEffectBlur
----------------

macOS blur effect for frosted glass appearance.

.. code-block:: python

    nib.VisualEffectBlur(
        style=nib.BlurStyle.DARK,
        content=nib.VStack(
            controls=[
                nib.Text("Blurred Background"),
            ],
            padding=20,
        ),
    )

**Blur Styles:**

- ``ULTRA_THIN_MATERIAL`` - Very subtle blur
- ``THIN_MATERIAL`` - Subtle blur
- ``REGULAR_MATERIAL`` - Standard blur
- ``THICK_MATERIAL`` - Heavy blur
- ``ULTRA_THICK_MATERIAL`` - Very heavy blur
- ``DARK`` - Dark vibrancy
- ``LIGHT`` - Light vibrancy
- ``MEDIUM_LIGHT`` - Medium light vibrancy

Example: Floating Card
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    nib.ZStack(controls=[
        nib.Image(name="background.jpg"),  # Behind
        nib.VisualEffectBlur(
            style=nib.BlurStyle.REGULAR_MATERIAL,
            content=nib.VStack(
                controls=[
                    nib.Text("Floating Card", font=nib.Font.HEADLINE),
                    nib.Text("Content on blur"),
                ],
                padding=16,
            ),
        ),
    ])

Modifiers for Effects
---------------------

All views support these effect-related modifiers:

Opacity
~~~~~~~

.. code-block:: python

    nib.Text("Faded", opacity=0.5)

Shadow
~~~~~~

.. code-block:: python

    nib.Rectangle(
        corner_radius=12,
        fill="#FFFFFF",
        shadow_color="#000000",
        shadow_radius=10,
        shadow_x=0,
        shadow_y=4,
    )

Blur
~~~~

.. code-block:: python

    nib.Image(
        name="photo.jpg",
        blur_radius=5,
    )

Saturation
~~~~~~~~~~

.. code-block:: python

    nib.Image(
        name="photo.jpg",
        saturation=0,  # Grayscale
    )

Brightness & Contrast
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    nib.Image(
        name="photo.jpg",
        brightness=0.2,   # -1 to 1
        contrast=1.5,     # 0 to 2
    )
