Toggle
======

A control for switching between on and off states.

.. code-block:: python

    nib.Toggle(
        "Enable Notifications",
        value=True,
        on_change=lambda is_on: print(f"Toggle: {is_on}"),
    )

.. autoclass:: nib.Toggle
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``label`` - Text label for the toggle
- ``value`` - Current on/off state
- ``on_change`` - Callback when toggled
- ``style`` - Toggle style (:class:`~nib.ToggleStyle`)

Examples
--------

**Basic Toggle**

.. code-block:: python

    nib.Toggle("Dark Mode", value=False)

**With Change Handler**

.. code-block:: python

    def on_toggle(is_on: bool):
        print(f"Notifications: {'enabled' if is_on else 'disabled'}")

    nib.Toggle(
        "Enable Notifications",
        value=True,
        on_change=on_toggle,
    )

**Settings List**

.. code-block:: python

    nib.List(
        controls=[
            nib.Toggle("Wi-Fi", value=True),
            nib.Toggle("Bluetooth", value=True),
            nib.Toggle("Airplane Mode", value=False),
        ],
    )

**Checkbox Style**

.. code-block:: python

    nib.Toggle(
        "I agree to the terms",
        value=False,
        style=nib.ToggleStyle.CHECKBOX,
    )

**Switch Style (Default)**

.. code-block:: python

    nib.Toggle(
        "Auto-save",
        value=True,
        style=nib.ToggleStyle.SWITCH,
    )

**Reactive Toggle**

.. code-block:: python

    dark_mode = nib.Toggle("Dark Mode", value=False)

    def check_state():
        if dark_mode.value:
            print("Dark mode is on")
        else:
            print("Dark mode is off")
