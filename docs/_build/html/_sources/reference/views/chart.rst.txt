Chart
=====

A container for displaying data visualizations using Swift Charts.

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(x="Jan", y=100),
            nib.BarMark(x="Feb", y=150),
            nib.BarMark(x="Mar", y=120),
        ],
    )

.. autoclass:: nib.Chart
   :members:
   :undoc-members:
   :show-inheritance:

Parameters
----------

- ``marks`` - List of chart marks (BarMark, LineMark, etc.)
- ``x_axis`` - X-axis configuration (:class:`~nib.ChartAxis`)
- ``y_axis`` - Y-axis configuration (:class:`~nib.ChartAxis`)
- ``legend`` - Legend configuration (:class:`~nib.ChartLegend`)

ChartAxis
---------

.. autoclass:: nib.ChartAxis
   :members:
   :undoc-members:

ChartLegend
-----------

.. autoclass:: nib.ChartLegend
   :members:
   :undoc-members:

Examples
--------

**Simple Bar Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.BarMark(x="Q1", y=1000),
            nib.BarMark(x="Q2", y=1500),
            nib.BarMark(x="Q3", y=1200),
            nib.BarMark(x="Q4", y=1800),
        ],
        width=300,
        height=200,
    )

**Line Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.LineMark(x=0, y=10),
            nib.LineMark(x=1, y=25),
            nib.LineMark(x=2, y=18),
            nib.LineMark(x=3, y=32),
        ],
    )

**Area Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.AreaMark(x=i, y=v)
            for i, v in enumerate([10, 25, 15, 30, 20])
        ],
    )

**With Axis Configuration**

.. code-block:: python

    nib.Chart(
        marks=[...],
        x_axis=nib.ChartAxis(label="Month"),
        y_axis=nib.ChartAxis(label="Sales ($)"),
    )

**Hide Axes**

.. code-block:: python

    nib.Chart(
        marks=[...],
        x_axis=nib.ChartAxis(hidden=True),
        y_axis=nib.ChartAxis(hidden=True),
    )

**With Legend**

.. code-block:: python

    nib.Chart(
        marks=[...],
        legend=nib.ChartLegend(position="bottom"),
    )

**Pie Chart**

.. code-block:: python

    nib.Chart(
        marks=[
            nib.SectorMark(value=30, label="iOS"),
            nib.SectorMark(value=45, label="Android"),
            nib.SectorMark(value=25, label="Web"),
        ],
    )
