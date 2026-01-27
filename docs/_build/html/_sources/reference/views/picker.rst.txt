Picker
======

A control for selecting from a set of options.

.. code-block:: python

    nib.Picker(
        selection="option1",
        options=["option1", "option2", "option3"],
        on_change=lambda value: print(f"Selected: {value}"),
    )

.. autoclass:: nib.Picker
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``selection`` - Currently selected value
- ``options`` - List of option values
- ``labels`` - Optional display labels (if different from values)
- ``label`` - Optional picker label
- ``on_change`` - Callback when selection changes
- ``style`` - Picker style (:class:`~nib.PickerStyle`)

Examples
--------

**Basic Picker**

.. code-block:: python

    nib.Picker(
        selection="medium",
        options=["small", "medium", "large"],
    )

**With Labels**

.. code-block:: python

    nib.Picker(
        selection="md",
        options=["sm", "md", "lg"],
        labels=["Small", "Medium", "Large"],
    )

**With Change Handler**

.. code-block:: python

    def on_size_change(size: str):
        print(f"Selected size: {size}")

    nib.Picker(
        selection="medium",
        options=["small", "medium", "large"],
        on_change=on_size_change,
    )

**Segmented Style**

.. code-block:: python

    nib.Picker(
        selection="day",
        options=["day", "week", "month"],
        labels=["Day", "Week", "Month"],
        style=nib.PickerStyle.SEGMENTED,
    )

**Menu Style**

.. code-block:: python

    nib.Picker(
        label="Country",
        selection="us",
        options=["us", "uk", "de", "fr"],
        labels=["United States", "United Kingdom", "Germany", "France"],
        style=nib.PickerStyle.MENU,
    )

**In a Form**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Picker(
                label="Theme",
                selection="system",
                options=["light", "dark", "system"],
                labels=["Light", "Dark", "System"],
            ),
            nib.Picker(
                label="Language",
                selection="en",
                options=["en", "es", "fr"],
                labels=["English", "Spanish", "French"],
            ),
        ],
        spacing=12,
    )
