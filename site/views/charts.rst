Charts
======

SwiftUI Charts for data visualization.

Chart Container
---------------

All chart marks must be wrapped in a ``Chart`` container.

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(x="Category", y="Value", data=data),
        ],
        width=300,
        height=200,
    )

Line Charts
-----------

LineMark
~~~~~~~~

.. code-block:: python

    data = [
        {"month": "Jan", "sales": 100},
        {"month": "Feb", "sales": 120},
        {"month": "Mar", "sales": 95},
        {"month": "Apr", "sales": 140},
    ]

    nib.Chart(
        marks=[
            nib.LineMark(x="month", y="sales", data=data),
        ],
    )

With multiple series:

.. code-block:: python

    data = [
        {"month": "Jan", "product": "A", "sales": 100},
        {"month": "Jan", "product": "B", "sales": 80},
        {"month": "Feb", "product": "A", "sales": 120},
        {"month": "Feb", "product": "B", "sales": 90},
    ]

    nib.Chart(
        marks=[
            nib.LineMark(
                x="month",
                y="sales",
                series="product",  # Color by product
                data=data,
            ),
        ],
    )

**LineMark Parameters:**

- ``interpolation`` - ``LINEAR``, ``CARDINAL``, ``CATMULL_ROM``, ``MONOTONE``, ``STEP_START``, ``STEP_CENTER``, ``STEP_END``
- ``symbol`` - Point symbol: ``CIRCLE``, ``SQUARE``, ``TRIANGLE``, ``DIAMOND``, ``CROSS``, ``PLUS``

Bar Charts
----------

BarMark
~~~~~~~

.. code-block:: python

    data = [
        {"category": "A", "value": 50},
        {"category": "B", "value": 30},
        {"category": "C", "value": 70},
    ]

    nib.Chart(
        marks=[
            nib.BarMark(x="category", y="value", data=data),
        ],
    )

Stacked bars:

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(
                x="month",
                y="sales",
                series="product",
                data=data,
                stacking=nib.StackingMethod.STANDARD,
            ),
        ],
    )

**StackingMethod:** ``STANDARD``, ``NORMALIZED``, ``CENTER``, ``UNSTACKED``

Area Charts
-----------

AreaMark
~~~~~~~~

.. code-block:: python

    nib.Chart(
        marks=[
            nib.AreaMark(
                x="time",
                y="value",
                data=data,
                opacity=0.5,
            ),
        ],
    )

Point Charts
------------

PointMark
~~~~~~~~~

Scatter plots and point annotations.

.. code-block:: python

    data = [
        {"x": 1, "y": 2, "size": 10},
        {"x": 3, "y": 5, "size": 20},
        {"x": 5, "y": 3, "size": 15},
    ]

    nib.Chart(
        marks=[
            nib.PointMark(
                x="x",
                y="y",
                data=data,
                symbol=nib.SymbolShape.CIRCLE,
            ),
        ],
    )

Pie/Donut Charts
----------------

SectorMark
~~~~~~~~~~

.. code-block:: python

    data = [
        {"category": "A", "value": 30},
        {"category": "B", "value": 45},
        {"category": "C", "value": 25},
    ]

    nib.Chart(
        marks=[
            nib.SectorMark(
                angle="value",
                color="category",
                data=data,
            ),
        ],
    )

Donut chart (with inner radius):

.. code-block:: python

    nib.Chart(
        marks=[
            nib.SectorMark(
                angle="value",
                color="category",
                inner_radius_ratio=0.5,  # 50% inner radius
                data=data,
            ),
        ],
    )

Reference Lines
---------------

RuleMark
~~~~~~~~

.. code-block:: python

    nib.Chart(
        marks=[
            nib.LineMark(x="date", y="value", data=data),
            # Horizontal reference line
            nib.RuleMark(y=100, stroke_style="dashed"),
            # Vertical reference line
            nib.RuleMark(x="2024-06-01"),
        ],
    )

RectMark
~~~~~~~~

Highlight regions in charts.

.. code-block:: python

    nib.Chart(
        marks=[
            nib.LineMark(x="date", y="value", data=data),
            nib.RectMark(
                x_start="2024-01-01",
                x_end="2024-03-01",
                fill="#FF000022",  # Semi-transparent red
            ),
        ],
    )

Chart Configuration
-------------------

Axis
~~~~

.. code-block:: python

    nib.Chart(
        marks=[...],
        x_axis=nib.ChartAxis(
            label="Time",
            hidden=False,
        ),
        y_axis=nib.ChartAxis(
            label="Value",
            position="leading",
        ),
    )

Legend
~~~~~~

.. code-block:: python

    nib.Chart(
        marks=[...],
        legend=nib.ChartLegend(
            position="bottom",
            hidden=False,
        ),
    )

Combining Marks
---------------

Layer multiple mark types:

.. code-block:: python

    nib.Chart(
        marks=[
            # Area as background
            nib.AreaMark(x="date", y="value", data=data, opacity=0.3),
            # Line on top
            nib.LineMark(x="date", y="value", data=data),
            # Points at data values
            nib.PointMark(x="date", y="value", data=data),
            # Reference line
            nib.RuleMark(y=average_value, stroke="#FF0000"),
        ],
    )
