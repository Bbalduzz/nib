Slider
======

A control for selecting a value from a continuous range.

.. code-block:: python

    nib.Slider(
        value=50,
        range=(0, 100),
        on_change=lambda v: print(f"Value: {v}"),
    )

.. autoclass:: nib.Slider
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``value`` - Current value
- ``range`` - Tuple of (min, max) values
- ``step`` - Step increment (optional)
- ``on_change`` - Callback when value changes
- ``label`` - Optional label text

Examples
--------

**Basic Slider**

.. code-block:: python

    nib.Slider(value=50, range=(0, 100))

**With Change Handler**

.. code-block:: python

    def on_volume_change(volume: float):
        print(f"Volume: {volume}%")

    nib.Slider(
        value=75,
        range=(0, 100),
        on_change=on_volume_change,
    )

**With Step**

.. code-block:: python

    nib.Slider(
        value=50,
        range=(0, 100),
        step=10,  # Only allows 0, 10, 20, ..., 100
    )

**Volume Control**

.. code-block:: python

    volume_label = nib.Text("50%")

    def update_volume(value: float):
        volume_label.content = f"{int(value)}%"

    nib.VStack(
        controls=[
            nib.HStack(
                controls=[
                    nib.Label("Volume", system_image="speaker.wave.2"),
                    nib.Spacer(),
                    volume_label,
                ],
            ),
            nib.Slider(
                value=50,
                range=(0, 100),
                on_change=update_volume,
            ),
        ],
        spacing=8,
    )

**Brightness Control**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Label("", system_image="sun.min"),
            nib.Slider(value=80, range=(0, 100)),
            nib.Label("", system_image="sun.max"),
        ],
        spacing=8,
    )
