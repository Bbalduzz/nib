Spacer
======

A flexible space that expands to fill available space in a stack.

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Left"),
            nib.Spacer(),
            nib.Text("Right"),
        ],
    )

.. autoclass:: nib.Spacer
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``min_length`` - Minimum length of the spacer (optional)

Examples
--------

**Push Content Apart**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Title"),
            nib.Spacer(),
            nib.Button("Action", action=do_action),
        ],
    )

**Center Content**

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Spacer(),
            nib.Text("Centered"),
            nib.Spacer(),
        ],
    )

**With Minimum Length**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Top"),
            nib.Spacer(min_length=50),
            nib.Text("Bottom with at least 50pt gap"),
        ],
    )

**Push to Bottom**

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("Header"),
            nib.Spacer(),
            nib.Button("Action at Bottom", action=action),
        ],
        padding=16,
    )
