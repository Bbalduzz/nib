Divider
=======

A visual separator line between views.

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Section 1"),
            nib.Divider(),
            nib.Text("Section 2"),
        ],
    )

.. autoclass:: nib.Divider
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

**Basic Divider**

.. code-block:: python

    nib.Divider()

**In Vertical Stack**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Header"),
            nib.Divider(),
            nib.Text("Content"),
            nib.Divider(),
            nib.Text("Footer"),
        ],
        spacing=8,
    )

**In Horizontal Stack**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Left"),
            nib.Divider(),
            nib.Text("Right"),
        ],
        spacing=8,
    )

**Styled Divider**

.. code-block:: python

    nib.Divider(
        foreground_color="#444",
        padding={"horizontal": 16},
    )

**Menu-like List**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Label("Settings", system_image="gear"),
            nib.Label("Profile", system_image="person"),
            nib.Divider(),
            nib.Label("Logout", system_image="arrow.right.square"),
        ],
        spacing=4,
    )
