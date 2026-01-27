Chart Marks
===========

Marks are the visual elements that represent data in a chart.

LineMark
--------

A mark that displays data as a line connecting points.

.. code-block:: python

    nib.LineMark(x=1, y=100)
    nib.LineMark(x=1, y=100, series="Series A")

.. autoclass:: nib.LineMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Line Chart**

.. code-block:: python

    data = [(0, 10), (1, 25), (2, 15), (3, 30)]
    nib.Chart(
        marks=[nib.LineMark(x=x, y=y) for x, y in data],
    )

**Example: Multi-series Line Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.LineMark(x=0, y=10, series="A"),
            nib.LineMark(x=1, y=20, series="A"),
            nib.LineMark(x=0, y=15, series="B"),
            nib.LineMark(x=1, y=25, series="B"),
        ],
    )

BarMark
-------

A mark that displays data as rectangular bars.

.. code-block:: python

    nib.BarMark(x="Jan", y=100)
    nib.BarMark(x="Jan", y=100, series="Product A")

.. autoclass:: nib.BarMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Bar Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(x="Q1", y=1000),
            nib.BarMark(x="Q2", y=1500),
            nib.BarMark(x="Q3", y=1200),
        ],
    )

**Example: Grouped Bar Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(x="Jan", y=100, series="2023"),
            nib.BarMark(x="Jan", y=120, series="2024"),
            nib.BarMark(x="Feb", y=150, series="2023"),
            nib.BarMark(x="Feb", y=180, series="2024"),
        ],
    )

AreaMark
--------

A mark that displays data as a filled area.

.. code-block:: python

    nib.AreaMark(x=1, y=100)

.. autoclass:: nib.AreaMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Area Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.AreaMark(x=i, y=v)
            for i, v in enumerate([10, 25, 15, 30, 20])
        ],
    )

PointMark
---------

A mark that displays data as individual points.

.. code-block:: python

    nib.PointMark(x=1, y=100)

.. autoclass:: nib.PointMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Scatter Plot**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.PointMark(x=x, y=y)
            for x, y in scatter_data
        ],
    )

RuleMark
--------

A mark that displays a horizontal or vertical rule line.

.. code-block:: python

    nib.RuleMark(y=50)  # Horizontal line at y=50
    nib.RuleMark(x=10)  # Vertical line at x=10

.. autoclass:: nib.RuleMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Reference Line**

.. code-block:: python

    nib.Chart(
        marks=[
            *[nib.BarMark(x=m, y=v) for m, v in monthly_data],
            nib.RuleMark(y=average, stroke=nib.Color.RED),
        ],
    )

RectMark
--------

A mark that displays data as rectangles (for heatmaps).

.. autoclass:: nib.RectMark
   :members:
   :undoc-members:
   :show-inheritance:

SectorMark
----------

A mark for pie/donut charts.

.. code-block:: python

    nib.SectorMark(value=30, label="Category A")

.. autoclass:: nib.SectorMark
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Pie Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.SectorMark(value=30, label="iOS"),
            nib.SectorMark(value=45, label="Android"),
            nib.SectorMark(value=25, label="Web"),
        ],
    )

Enums
-----

InterpolationMethod
^^^^^^^^^^^^^^^^^^^

.. autoclass:: nib.InterpolationMethod
   :members:
   :undoc-members:

StackingMethod
^^^^^^^^^^^^^^

.. autoclass:: nib.StackingMethod
   :members:
   :undoc-members:

SymbolShape
^^^^^^^^^^^

.. autoclass:: nib.SymbolShape
   :members:
   :undoc-members:
