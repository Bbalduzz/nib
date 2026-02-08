# Charts

Nib integrates with Swift Charts to provide native, GPU-accelerated data visualizations. You define charts using a declarative API: provide your data as a list of dictionaries, and specify mark types that map data fields to visual properties.

## Creating a chart

```python
import nib

chart = nib.Chart(
    data=[
        {"month": "Jan", "sales": 100},
        {"month": "Feb", "sales": 150},
        {"month": "Mar", "sales": 200},
        {"month": "Apr", "sales": 175},
        {"month": "May", "sales": 250},
    ],
    marks=[nib.LineMark(x="month", y="sales")],
    width=350,
    height=220,
)
```

The `Chart` constructor takes:

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `list[dict]` | List of data rows as dictionaries |
| `marks` | `list[BaseMark]` | List of mark objects defining the visualization |
| `x_axis` | `ChartAxis` | X-axis configuration (optional) |
| `y_axis` | `ChartAxis` | Y-axis configuration (optional) |
| `legend` | `ChartLegend` or `bool` | Legend configuration, or `False` to hide |
| `chart_background` | `str` | Background color for the entire chart |
| `plot_background` | `str` | Background color for the plot area only |

Standard view modifiers (`width`, `height`, `padding`, `corner_radius`, etc.) are also supported.

## Data format

Data is a list of dictionaries where each dictionary represents a row. The keys correspond to the field names used in your marks:

```python
data = [
    {"month": "Jan", "revenue": 4200, "expenses": 3100},
    {"month": "Feb", "revenue": 5100, "expenses": 3400},
    {"month": "Mar", "revenue": 4800, "expenses": 3200},
]
```

!!! note
    Nib converts row-based data to a columnar format internally for efficient serialization. You always work with the row-based format in your Python code.

## Mark types

### LineMark

Connects data points with a continuous line. Best for trends over time:

```python
nib.LineMark(x="month", y="sales")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `str` or `PlottableField` | Data field for x-axis |
| `y` | `str` or `PlottableField` | Data field for y-axis |
| `foreground_style` | `str` or `PlottableField` | Line color or field for multi-series |
| `symbol` | `SymbolShape` or `PlottableField` | Marker shape at each point |
| `interpolation` | `InterpolationMethod` | Curve type between points |
| `line_width` | `float` | Line width in points |
| `opacity` | `float` | Opacity from 0.0 to 1.0 |

### BarMark

Displays data as rectangular bars. Best for comparing categories:

```python
nib.BarMark(x="category", y="value")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `str` or `PlottableField` | Data field for x-axis |
| `y` | `str` or `PlottableField` | Data field for y-axis |
| `width` | `float` | Fixed bar width in points |
| `height` | `float` | Fixed bar height in points |
| `foreground_style` | `str` or `PlottableField` | Bar color or field for grouping |
| `stacking` | `StackingMethod` | Stacking mode for multi-series |
| `corner_radius` | `float` | Rounded corner radius |
| `opacity` | `float` | Opacity from 0.0 to 1.0 |

### AreaMark

Fills the region between a line and a baseline:

```python
nib.AreaMark(x="date", y="revenue", foreground_style="#3B82F6", opacity=0.3)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `str` or `PlottableField` | Data field for x-axis |
| `y` | `str` or `PlottableField` | Data field for upper boundary |
| `y_start` | `str` or `PlottableField` | Data field for lower boundary (optional) |
| `foreground_style` | `str` or `PlottableField` | Fill color or field for multi-series |
| `interpolation` | `InterpolationMethod` | Curve type |
| `stacking` | `StackingMethod` | Stacking mode |
| `opacity` | `float` | Opacity from 0.0 to 1.0 |

### PointMark

Displays individual data points as symbols. Best for scatter plots:

```python
nib.PointMark(x="height", y="weight", foreground_style="#EF4444")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | `str` or `PlottableField` | Data field for x-axis |
| `y` | `str` or `PlottableField` | Data field for y-axis |
| `foreground_style` | `str` or `PlottableField` | Point color or field for coloring |
| `symbol` | `SymbolShape` or `PlottableField` | Marker shape |
| `symbol_size` | `float` | Marker size in square points |
| `opacity` | `float` | Opacity from 0.0 to 1.0 |

### SectorMark

Creates pie and donut charts:

```python
nib.SectorMark(
    angle="value",
    foreground_style=nib.PlottableField("category"),
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `angle` | `str` or `PlottableField` | Data field for sector sizes |
| `foreground_style` | `str` or `PlottableField` | Color or field for per-segment colors |
| `inner_radius` | `float` | Inner radius (0 = pie, >0 = donut) |
| `outer_radius` | `float` | Outer radius |
| `corner_radius` | `float` | Rounded segment corners |
| `opacity` | `float` | Opacity from 0.0 to 1.0 |

### RuleMark

Draws a reference line (horizontal or vertical):

```python
# Horizontal line at y=100
nib.RuleMark(y=100, foreground_style="#EF4444", line_width=2)

# Vertical line at x position
nib.RuleMark(x="2024-06-15", foreground_style="#6366F1")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | value or field | X position for vertical rule |
| `y` | value or field | Y position for horizontal rule |
| `x_start` / `x_end` | value or field | Horizontal bounds for segments |
| `y_start` / `y_end` | value or field | Vertical bounds for segments |
| `foreground_style` | `str` or `PlottableField` | Line color |
| `line_width` | `float` | Line width |

### RectMark

Draws filled rectangles for heatmaps and range charts:

```python
nib.RectMark(
    x="weekday", y="hour",
    foreground_style=nib.PlottableField("intensity"),
    corner_radius=2,
)
```

## PlottableField

Use `PlottableField` to reference data columns with optional type hints:

```python
from nib import PlottableField

# Simple field reference (equivalent to just passing "month")
nib.LineMark(x=PlottableField("month"), y=PlottableField("sales"))

# With type hint for proper scale selection
nib.LineMark(
    x=PlottableField("date", type="temporal"),
    y=PlottableField("temperature", type="quantitative"),
)
```

Available types: `"quantitative"` (numeric), `"nominal"` (categorical), `"temporal"` (dates/times).

## Multiple series

To display multiple data series with automatic color assignment, pass a `PlottableField` as `foreground_style`:

```python
data = [
    {"month": "Jan", "value": 100, "series": "Revenue"},
    {"month": "Jan", "value": 80, "series": "Expenses"},
    {"month": "Feb", "value": 150, "series": "Revenue"},
    {"month": "Feb", "value": 90, "series": "Expenses"},
    {"month": "Mar", "value": 200, "series": "Revenue"},
    {"month": "Mar", "value": 110, "series": "Expenses"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.LineMark(
            x="month",
            y="value",
            foreground_style=nib.PlottableField("series"),
        ),
    ],
    width=350,
    height=220,
)
```

Swift Charts automatically assigns distinct colors to each unique value in the `series` field.

## Combining marks

Combine multiple mark types in a single chart for layered visualizations:

```python
chart = nib.Chart(
    data=data,
    marks=[
        nib.AreaMark(x="month", y="sales", foreground_style="#3B82F6", opacity=0.2),
        nib.LineMark(x="month", y="sales", foreground_style="#3B82F6"),
        nib.PointMark(x="month", y="sales", foreground_style="#3B82F6"),
        nib.RuleMark(y=150, foreground_style="#EF4444", line_width=1),
    ],
    width=350,
    height=220,
)
```

This creates an area chart with a line overlay, point markers at each data point, and a horizontal reference line at y=150.

## Axis configuration

Use `ChartAxis` to customize axis appearance:

```python
chart = nib.Chart(
    data=data,
    marks=[nib.BarMark(x="month", y="revenue")],
    x_axis=nib.ChartAxis(
        label="Month",
        position="bottom",
    ),
    y_axis=nib.ChartAxis(
        label="Revenue ($)",
        grid_lines=True,
        format="currency",
        grid_color="#333333",
        label_color="#666666",
    ),
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `str` | `None` | Axis label text |
| `position` | `str` | auto | `"bottom"`, `"top"`, `"leading"`, or `"trailing"` |
| `grid_lines` | `bool` | `False` | Show grid lines |
| `hidden` | `bool` | `False` | Hide the axis entirely |
| `format` | `str` | auto | `"number"`, `"currency"`, or `"percent"` |
| `values` | `list` | `None` | Explicit tick mark values |
| `label_color` | `str` | `None` | Color for axis labels |
| `grid_color` | `str` | `None` | Color for grid lines |

## Legend configuration

Control the chart legend with `ChartLegend`:

```python
chart = nib.Chart(
    data=data,
    marks=[nib.LineMark(x="month", y="value", foreground_style=nib.PlottableField("series"))],
    legend=nib.ChartLegend(
        position="bottom",
        title="Category",
    ),
)

# Or hide the legend entirely
chart = nib.Chart(
    data=data,
    marks=[...],
    legend=False,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `position` | `str` | `"top"`, `"bottom"`, `"leading"`, `"trailing"`, or `"automatic"` |
| `hidden` | `bool` | Hide the legend |
| `title` | `str` | Title text displayed above legend items |

## InterpolationMethod

Control how lines and areas are drawn between data points:

```python
nib.LineMark(
    x="month", y="sales",
    interpolation=nib.InterpolationMethod.MONOTONE,
)
```

| Value | Description |
|-------|-------------|
| `LINEAR` | Straight lines between points (default) |
| `MONOTONE` | Smooth curve that preserves monotonicity |
| `CATMULL_ROM` | Smooth cubic spline through all points |
| `CARDINAL` | Smooth curve with adjustable tension |
| `STEP_START` | Step at the start of each interval |
| `STEP_CENTER` | Step at the midpoint between points |
| `STEP_END` | Step at the end of each interval |

## StackingMethod

Control how overlapping bars or areas are stacked:

```python
nib.BarMark(
    x="month", y="sales",
    foreground_style=nib.PlottableField("region"),
    stacking=nib.StackingMethod.STANDARD,
)
```

| Value | Description |
|-------|-------------|
| `STANDARD` | Stack values on top of each other |
| `NORMALIZED` | Scale stacks to 100% |
| `CENTER` | Center stacks (stream graph effect) |

## SymbolShape

Marker shapes for `PointMark` and `LineMark`:

```python
nib.PointMark(x="x", y="y", symbol=nib.SymbolShape.DIAMOND)
```

Available shapes: `CIRCLE`, `SQUARE`, `TRIANGLE`, `DIAMOND`, `CROSS`, `PLUS`, `PENTAGON`, `HEXAGON`.

## Reactive data updates

Chart data is reactive. Updating it triggers an automatic re-render:

```python
# Replace all data
chart.data = new_data

# Append a single row
chart.append_data({"month": "Jun", "sales": 300})

# Update a specific row
chart.update_data(0, {"month": "Jan", "sales": 120})

# Clear all data
chart.clear_data()
```

## Complete example

A sales dashboard with a bar chart, trend line, and live data updates:

```python
import nib
import random


def main(app: nib.App):
    app.title = "Sales"
    app.icon = nib.SFSymbol("chart.bar.fill")
    app.width = 400
    app.height = 450

    data = [
        {"month": "Jan", "sales": 120, "target": 100},
        {"month": "Feb", "sales": 150, "target": 130},
        {"month": "Mar", "sales": 180, "target": 160},
        {"month": "Apr", "sales": 160, "target": 170},
        {"month": "May", "sales": 210, "target": 190},
        {"month": "Jun", "sales": 240, "target": 220},
    ]

    chart = nib.Chart(
        data=data,
        marks=[
            nib.BarMark(
                x="month", y="sales",
                foreground_style="#3B82F6",
                corner_radius=4,
            ),
            nib.LineMark(
                x="month", y="target",
                foreground_style="#EF4444",
                line_width=2,
                symbol=nib.SymbolShape.CIRCLE,
                interpolation=nib.InterpolationMethod.MONOTONE,
            ),
        ],
        x_axis=nib.ChartAxis(label="Month"),
        y_axis=nib.ChartAxis(
            label="Units Sold",
            grid_lines=True,
            grid_color="#e5e7eb",
        ),
        chart_background="#ffffff",
        width=370,
        height=250,
        padding=8,
        corner_radius=12,
    )

    total_label = nib.Text(
        f"Total: {sum(d['sales'] for d in data)} units",
        font=nib.Font.HEADLINE,
    )

    # Donut chart for breakdown
    pie_data = [
        {"category": "Online", "value": 450},
        {"category": "Retail", "value": 320},
        {"category": "Wholesale", "value": 290},
    ]

    donut = nib.Chart(
        data=pie_data,
        marks=[
            nib.SectorMark(
                angle="value",
                foreground_style=nib.PlottableField("category"),
                inner_radius=40,
                outer_radius=70,
                corner_radius=3,
            ),
        ],
        legend=nib.ChartLegend(position="bottom"),
        width=370,
        height=160,
    )

    app.build(
        nib.VStack(
            controls=[
                total_label,
                chart,
                nib.Text("Sales by Channel", font=nib.Font.SUBHEADLINE),
                donut,
            ],
            spacing=12,
            padding=16,
        )
    )


nib.run(main)
```
