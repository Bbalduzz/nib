Buttons & Controls
==================

Interactive controls for user input.

Button
------

Clickable button that triggers an action.

.. code-block:: python

    def on_click():
        print("Clicked!")

    nib.Button("Click Me", action=on_click)

**Styled Buttons:**

.. code-block:: python

    # Primary action (prominent)
    nib.Button(
        "Save",
        action=save,
        style=nib.ButtonStyle.BORDEREDPROMINENT,
    )

    # Secondary action
    nib.Button(
        "Cancel",
        action=cancel,
        style=nib.ButtonStyle.BORDERED,
    )

    # Plain text button
    nib.Button(
        "Learn More",
        action=learn_more,
        style=nib.ButtonStyle.PLAIN,
    )

    # Destructive action (red tint)
    nib.Button(
        "Delete",
        action=delete,
        role=nib.ButtonRole.DESTRUCTIVE,
    )

**Button Sizes:**

.. code-block:: python

    nib.Button("Small", action=fn, control_size=nib.ControlSize.SMALL)
    nib.Button("Regular", action=fn, control_size=nib.ControlSize.REGULAR)
    nib.Button("Large", action=fn, control_size=nib.ControlSize.LARGE)

**Parameters:**

- ``label`` - Button text
- ``action`` - Callback function
- ``style`` - ``AUTOMATIC``, ``BORDERED``, ``BORDEREDPROMINENT``, ``BORDERLESS``, ``PLAIN``, ``LINK``
- ``role`` - ``DESTRUCTIVE``, ``CANCEL``
- ``control_size`` - ``MINI``, ``SMALL``, ``REGULAR``, ``LARGE``, ``EXTRA_LARGE``

Toggle
------

On/off switch control.

.. code-block:: python

    def on_toggle(is_on: bool):
        print(f"Toggle is {'on' if is_on else 'off'}")

    toggle = nib.Toggle(
        "Enable Notifications",
        value=True,
        on_change=on_toggle,
    )

    # Read current state
    print(toggle.value)

    # Set programmatically
    toggle.value = False

Slider
------

Value slider for numeric input.

.. code-block:: python

    def on_slide(value: float):
        print(f"Value: {value:.1f}")

    slider = nib.Slider(
        value=50,
        range=(0, 100),
        step=1,
        on_change=on_slide,
    )

    # With labels
    nib.Slider(
        value=0.5,
        range=(0, 1),
        label=nib.Text("Volume"),
        minimum_value_label=nib.Text("0%"),
        maximum_value_label=nib.Text("100%"),
    )

Picker
------

Selection from a list of options.

.. code-block:: python

    def on_pick(selection: str):
        print(f"Selected: {selection}")

    nib.Picker(
        selection="medium",
        options=["small", "medium", "large"],
        on_change=on_pick,
    )

    # With labels for display
    nib.Picker(
        selection="medium",
        options=["small", "medium", "large"],
        labels=["Small", "Medium", "Large"],
        label=nib.Text("Size"),
    )

**Picker Styles:**

.. code-block:: python

    nib.Picker(..., style=nib.PickerStyle.AUTOMATIC)
    nib.Picker(..., style=nib.PickerStyle.INLINE)
    nib.Picker(..., style=nib.PickerStyle.MENU)
    nib.Picker(..., style=nib.PickerStyle.SEGMENTED)
    nib.Picker(..., style=nib.PickerStyle.WHEEL)

Gauge
-----

Visual indicator for a value within a range.

.. code-block:: python

    # Simple gauge
    nib.Gauge(
        value=0.7,
        label=nib.Text("CPU"),
        current_value_label=nib.Text("70%"),
    )

    # With min/max labels
    nib.Gauge(
        value=75,
        range=(0, 100),
        label=nib.Text("Progress"),
        minimum_value_label=nib.Text("0"),
        maximum_value_label=nib.Text("100"),
        current_value_label=nib.Text("75"),
        style=nib.GaugeStyle.LINEAR_CAPACITY,
    )

**Gauge Styles:**

- ``AUTOMATIC`` - System default
- ``ACCESSORY_CIRCULAR`` - Compact circular
- ``ACCESSORY_CIRCULAR_CAPACITY`` - Circular with fill
- ``ACCESSORY_LINEAR`` - Horizontal bar
- ``ACCESSORY_LINEAR_CAPACITY`` - Horizontal bar with fill
- ``LINEAR_CAPACITY`` - Full-width horizontal bar

ProgressView
------------

Indeterminate or determinate progress indicator.

.. code-block:: python

    # Spinning (indeterminate)
    nib.ProgressView()

    # Determinate progress bar
    nib.ProgressView(
        value=0.5,  # 50% complete
        total=1.0,
        label=nib.Text("Downloading..."),
    )

ShareLink
---------

System share sheet for content.

.. code-block:: python

    nib.ShareLink(
        item="https://example.com",
        label=nib.Label("Share", system_image="square.and.arrow.up"),
    )

    # Share with preview
    nib.ShareLink(
        item="Check out this link!",
        preview_title="Cool Link",
        preview_image="preview.png",  # Asset image name
    )

Table
-----

Data table with columns and rows.

.. code-block:: python

    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    nib.Table(
        columns=[
            nib.TableColumn("name", title="Name"),
            nib.TableColumn("age", title="Age"),
        ],
        rows=data,
    )
