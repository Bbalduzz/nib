ScrollView
==========

A scrollable container for content that may exceed the available space.

.. code-block:: python

    nib.ScrollView(
        content=nib.VStack(
            controls=[nib.Text(f"Item {i}") for i in range(50)],
            spacing=8,
        ),
    )

.. autoclass:: nib.ScrollView
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``content`` - The view to display inside the scroll view
- ``axes`` - Scroll direction (:class:`~nib.ScrollAxis`)
- ``shows_indicators`` - Whether to show scroll indicators (default: True)

Examples
--------

**Vertical Scrolling (Default)**

.. code-block:: python

    nib.ScrollView(
        content=nib.VStack(
            controls=[
                nib.Text(f"Row {i}")
                for i in range(100)
            ],
            spacing=4,
        ),
    )

**Horizontal Scrolling**

.. code-block:: python

    nib.ScrollView(
        content=nib.HStack(
            controls=[
                nib.RoundedRectangle(
                    corner_radius=8,
                    fill=nib.Color.BLUE,
                    width=100,
                    height=100,
                )
                for _ in range(20)
            ],
            spacing=8,
        ),
        axes=nib.ScrollAxis.HORIZONTAL,
    )

**Hide Scroll Indicators**

.. code-block:: python

    nib.ScrollView(
        content=my_content,
        shows_indicators=False,
    )
