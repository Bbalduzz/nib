List
====

A container that displays rows of data in a single column with native list styling.

.. code-block:: python

    nib.List(
        controls=[
            nib.Text("Item 1"),
            nib.Text("Item 2"),
            nib.Text("Item 3"),
        ],
    )

.. autoclass:: nib.List
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``controls`` - List of child views to display as rows
- ``padding`` - Padding around the list

Examples
--------

**Simple List**

.. code-block:: python

    nib.List(
        controls=[
            nib.Text("Apple"),
            nib.Text("Banana"),
            nib.Text("Cherry"),
        ],
    )

**List with Complex Rows**

.. code-block:: python

    nib.List(
        controls=[
            nib.HStack(
                controls=[
                    nib.Label("Downloads", system_image="arrow.down.circle"),
                    nib.Spacer(),
                    nib.Text("5"),
                ],
            ),
            nib.HStack(
                controls=[
                    nib.Label("Uploads", system_image="arrow.up.circle"),
                    nib.Spacer(),
                    nib.Text("3"),
                ],
            ),
        ],
    )

**List with Sections**

.. code-block:: python

    nib.List(
        controls=[
            nib.Section(
                header=nib.Text("Fruits"),
                controls=[
                    nib.Text("Apple"),
                    nib.Text("Orange"),
                ],
            ),
            nib.Section(
                header=nib.Text("Vegetables"),
                controls=[
                    nib.Text("Carrot"),
                    nib.Text("Broccoli"),
                ],
            ),
        ],
    )
