Grid Layouts
============

Nib provides several grid layout views for arranging content in rows and columns.

LazyVGrid
---------

A vertically scrolling grid with configurable columns.

.. code-block:: python

    import nib

    # Three-column grid
    grid = nib.LazyVGrid(
        columns=[
            nib.GridItem(nib.GridItemSize.FLEXIBLE),
            nib.GridItem(nib.GridItemSize.FLEXIBLE),
            nib.GridItem(nib.GridItemSize.FLEXIBLE),
        ],
        controls=[
            nib.Text("1"), nib.Text("2"), nib.Text("3"),
            nib.Text("4"), nib.Text("5"), nib.Text("6"),
        ],
        spacing=10,
    )

GridItem Sizes
~~~~~~~~~~~~~~

.. code-block:: python

    # Fixed size columns (100 points each)
    nib.GridItem(nib.GridItemSize.FIXED, 100)

    # Flexible columns (expand to fill, minimum 50 points)
    nib.GridItem(nib.GridItemSize.FLEXIBLE, 50)

    # Adaptive columns (fit as many as possible, minimum 80 points each)
    nib.GridItem(nib.GridItemSize.ADAPTIVE, 80)

Convenience Functions
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from nib.views.layout.grid import fixed, flexible, adaptive

    columns = [
        fixed(100),           # Fixed 100pt column
        flexible(50),         # Flexible, min 50pt
        adaptive(80),         # Adaptive, min 80pt
    ]

LazyHGrid
---------

A horizontally scrolling grid with configurable rows.

.. code-block:: python

    import nib

    # Two-row horizontal grid
    grid = nib.LazyHGrid(
        rows=[
            nib.GridItem(nib.GridItemSize.FIXED, 50),
            nib.GridItem(nib.GridItemSize.FIXED, 50),
        ],
        controls=items,
        spacing=10,
    )

Grid
----

A fixed grid with explicit row structure using GridRow.

.. code-block:: python

    import nib

    # 2x2 grid
    grid = nib.Grid(
        controls=[
            nib.GridRow([nib.Text("A"), nib.Text("B")]),
            nib.GridRow([nib.Text("C"), nib.Text("D")]),
        ],
        horizontal_spacing=10,
        vertical_spacing=10,
    )

GridRow
-------

Defines a row within a Grid.

.. code-block:: python

    row = nib.GridRow(
        controls=[nib.Text("Col 1"), nib.Text("Col 2")],
        alignment="center",
    )

Example: Photo Grid
-------------------

.. code-block:: python

    import nib

    def main(app: nib.App):
        app.title = "Photo Grid"
        app.width = 350
        app.height = 400

        # Create colored squares as placeholder photos
        colors = [
            nib.Color.RED, nib.Color.ORANGE, nib.Color.YELLOW,
            nib.Color.GREEN, nib.Color.BLUE, nib.Color.PURPLE,
            nib.Color.PINK, nib.Color.CYAN, nib.Color.MINT,
        ]

        photos = [
            nib.RoundedRectangle(
                corner_radius=8,
                fill=color,
                width=100,
                height=100,
            )
            for color in colors
        ]

        app.build(
            nib.ScrollView(
                controls=[
                    nib.LazyVGrid(
                        columns=[
                            nib.GridItem(nib.GridItemSize.FLEXIBLE),
                            nib.GridItem(nib.GridItemSize.FLEXIBLE),
                            nib.GridItem(nib.GridItemSize.FLEXIBLE),
                        ],
                        controls=photos,
                        spacing=8,
                    )
                ],
                padding=16,
            )
        )

    nib.run(main)

Example: Adaptive Grid
----------------------

An adaptive grid automatically adjusts the number of columns based on available width:

.. code-block:: python

    import nib

    # Items will be at least 100pt wide, fitting as many as possible
    grid = nib.LazyVGrid(
        columns=[nib.GridItem(nib.GridItemSize.ADAPTIVE, 100)],
        controls=items,
        spacing=8,
    )
