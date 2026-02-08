Button
======

A control that initiates an action when tapped.

.. code-block:: python

    nib.Button("Click Me", action=on_click)

.. autoclass:: nib.Button
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``label`` - Button text
- ``action`` - Callback function when clicked
- ``style`` - Button style (:class:`~nib.ButtonStyle`)
- ``role`` - Button role (:class:`~nib.ButtonRole`)
- ``control_size`` - Button size (:class:`~nib.ControlSize`)

Examples
--------

**Basic Button**

.. code-block:: python

    def on_click():
        print("Button clicked!")

    nib.Button("Click Me", action=on_click)

**Styled Buttons**

.. code-block:: python

    # Primary action button
    nib.Button(
        "Save",
        action=save,
        style=nib.ButtonStyle.BORDEREDPROMINENT,
    )

    # Secondary button
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

**Destructive Button**

.. code-block:: python

    nib.Button(
        "Delete",
        action=delete,
        role=nib.ButtonRole.DESTRUCTIVE,
    )

**Button Sizes**

.. code-block:: python

    nib.Button("Small", action=action, control_size=nib.ControlSize.SMALL)
    nib.Button("Regular", action=action, control_size=nib.ControlSize.REGULAR)
    nib.Button("Large", action=action, control_size=nib.ControlSize.LARGE)

**Button Row**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Button("Cancel", action=cancel),
            nib.Spacer(),
            nib.Button(
                "Confirm",
                action=confirm,
                style=nib.ButtonStyle.BORDEREDPROMINENT,
            ),
        ],
        spacing=8,
    )
