Layout Views
============

Layout containers organize child views in various arrangements.

Stacks
------

VStack
~~~~~~

Arranges children vertically.

.. code-block:: python

    nib.VStack(
        controls=[
            nib.Text("First"),
            nib.Text("Second"),
            nib.Text("Third"),
        ],
        spacing=8,
        alignment=nib.HorizontalAlignment.LEADING,
    )

**Parameters:**

- ``controls`` - List of child views
- ``spacing`` - Space between children (default: 8)
- ``alignment`` - Horizontal alignment: ``LEADING``, ``CENTER``, ``TRAILING``

HStack
~~~~~~

Arranges children horizontally.

.. code-block:: python

    nib.HStack(
        controls=[
            nib.Text("Left"),
            nib.Spacer(),
            nib.Text("Right"),
        ],
        spacing=8,
        alignment=nib.VerticalAlignment.CENTER,
    )

**Parameters:**

- ``controls`` - List of child views
- ``spacing`` - Space between children (default: 8)
- ``alignment`` - Vertical alignment: ``TOP``, ``CENTER``, ``BOTTOM``, ``FIRST_TEXT_BASELINE``

ZStack
~~~~~~

Overlays children on top of each other (back to front).

.. code-block:: python

    nib.ZStack(
        controls=[
            nib.Rectangle(fill="#000000"),  # Background
            nib.Text("Overlay"),            # Foreground
        ],
        alignment=nib.Alignment.CENTER,
    )

Spacing & Dividers
------------------

Spacer
~~~~~~

Flexible space that expands to fill available room.

.. code-block:: python

    nib.HStack(controls=[
        nib.Text("Left"),
        nib.Spacer(),      # Pushes Right to the edge
        nib.Text("Right"),
    ])

Divider
~~~~~~~

Visual separator line.

.. code-block:: python

    nib.VStack(controls=[
        nib.Text("Section 1"),
        nib.Divider(),
        nib.Text("Section 2"),
    ])

Scrolling
---------

ScrollView
~~~~~~~~~~

Scrollable container for content that may overflow.

.. code-block:: python

    nib.ScrollView(
        content=nib.VStack(
            controls=[nib.Text(f"Item {i}") for i in range(50)],
        ),
        axis="vertical",  # or "horizontal", "both"
        show_indicators=True,
    )

List
~~~~

Optimized scrollable list for large datasets.

.. code-block:: python

    nib.List(
        controls=[
            nib.Text(f"Row {i}")
            for i in range(100)
        ],
        style=nib.ListStyle.INSET,
    )

**List Styles:** ``AUTOMATIC``, ``INSET``, ``INSET_GROUPED``, ``PLAIN``, ``SIDEBAR``

Section
~~~~~~~

Groups content with optional header and footer.

.. code-block:: python

    nib.Section(
        header=nib.Text("Settings"),
        controls=[
            nib.Toggle("Dark Mode", value=False),
            nib.Toggle("Notifications", value=True),
        ],
        footer=nib.Text("Configure app preferences"),
    )

Grids
-----

Grid
~~~~

CSS-like grid layout.

.. code-block:: python

    nib.Grid(
        controls=[
            nib.GridRow(controls=[
                nib.Text("A"),
                nib.Text("B"),
            ]),
            nib.GridRow(controls=[
                nib.Text("C"),
                nib.Text("D"),
            ]),
        ],
        horizontal_spacing=10,
        vertical_spacing=10,
    )

LazyVGrid / LazyHGrid
~~~~~~~~~~~~~~~~~~~~~

Grid that loads items lazily for performance.

.. code-block:: python

    nib.LazyVGrid(
        columns=[
            nib.GridItem(size=nib.GridItemSize.FLEXIBLE, minimum=100),
            nib.GridItem(size=nib.GridItemSize.FLEXIBLE, minimum=100),
        ],
        controls=[nib.Text(f"Item {i}") for i in range(20)],
        spacing=8,
    )

**GridItemSize:** ``FIXED(width)``, ``FLEXIBLE``, ``ADAPTIVE(minimum)``

Navigation
----------

NavigationStack
~~~~~~~~~~~~~~~

Container for hierarchical navigation.

.. code-block:: python

    nib.NavigationStack(
        content=nib.VStack(controls=[
            nib.NavigationLink(
                label=nib.Text("Go to Detail"),
                destination=nib.Text("Detail View"),
            ),
        ]),
    )

DisclosureGroup
~~~~~~~~~~~~~~~

Expandable/collapsible content section.

.. code-block:: python

    nib.DisclosureGroup(
        label=nib.Text("Advanced Options"),
        content=nib.VStack(controls=[
            nib.Toggle("Option 1", value=False),
            nib.Toggle("Option 2", value=True),
        ]),
        is_expanded=False,
    )

Group
~~~~~

Logical grouping without visual effect. Useful for applying modifiers to multiple views.

.. code-block:: python

    nib.Group(
        controls=[
            nib.Text("A"),
            nib.Text("B"),
        ],
        opacity=0.5,  # Applied to all children
    )
