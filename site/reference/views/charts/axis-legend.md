# ChartAxis & ChartLegend

Configuration objects for chart axes and legends. These are passed to the `Chart` constructor via the `x_axis`, `y_axis`, and `legend` parameters. They do not render anything on their own.

This page also documents the supporting types used for chart data encoding: `PlottableField`, `PlottableValue`, `InterpolationMethod`, `StackingMethod`, `SymbolShape`, `AxisPosition`, `LegendPosition`, and `PlottableType`.

---

## ChartAxis

Controls the appearance and behavior of a chart axis, including position, labels, grid lines, value formatting, and colors.

### Constructor

```python
nib.ChartAxis(
    position=None,
    label=None,
    grid_lines=None,
    hidden=None,
    format=None,
    values=None,
    label_color=None,
    grid_color=None,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | `str \| AxisPosition` | `None` | Position of the axis. For x-axis: `"bottom"` (default) or `"top"`. For y-axis: `"leading"` (default, left in LTR) or `"trailing"`. |
| `label` | `str` | `None` | Text label displayed alongside the axis (e.g., `"Temperature (F)"`). |
| `grid_lines` | `bool` | `None` | Whether to display grid lines extending from tick marks across the plot area. |
| `hidden` | `bool` | `None` | Whether to completely hide the axis, including tick marks and labels. |
| `format` | `str` | `None` | Format for axis values: `"number"`, `"currency"`, or `"percent"`. Defaults to automatic formatting. |
| `values` | `list` | `None` | Explicit list of values to show as tick marks. Only these values appear on the axis. |
| `label_color` | `str` | `None` | Color for axis labels and tick text. Accepts hex strings or named colors. |
| `grid_color` | `str` | `None` | Color for grid lines (when `grid_lines=True`). Accepts hex strings or named colors. |

### Examples

```python
# Basic axis with label
nib.ChartAxis(label="Revenue ($)")

# Axis with grid lines and formatting
nib.ChartAxis(
    label="Sales",
    grid_lines=True,
    format="currency",
    label_color="#666666",
    grid_color="#333333",
)

# Custom tick values
nib.ChartAxis(label="Rating", values=[1, 2, 3, 4, 5])

# Hidden axis
nib.ChartAxis(hidden=True)

# Axis positioned at top
nib.ChartAxis(position=nib.AxisPosition.TOP, label="Date")
```

---

## ChartLegend

Controls the position and visibility of the chart legend. The legend is automatically generated from `foreground_style` mappings in marks.

### Constructor

```python
nib.ChartLegend(
    position=None,
    hidden=None,
    title=None,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `position` | `str` | `None` | Legend position: `"top"`, `"bottom"`, `"leading"`, `"trailing"`, or `"automatic"`. |
| `hidden` | `bool` | `None` | Whether to hide the legend entirely. |
| `title` | `str` | `None` | Optional title text displayed above the legend items (e.g., `"Region"`). |

### Examples

```python
# Bottom-positioned legend with title
nib.ChartLegend(position="bottom", title="Product Category")

# Hide the legend
nib.ChartLegend(hidden=True)

# Or use the shorthand on Chart
nib.Chart(data=data, marks=[...], legend=False)
```

---

## PlottableField

A reference to a data column with optional type information. While field names can usually be passed as plain strings, `PlottableField` is useful when you need explicit data type hints or data-driven color/symbol encoding.

### Constructor

```python
nib.PlottableField(field, type=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field` | `str` | *required* | Name of the data column. Must match a key in the chart's data dictionaries. |
| `type` | `PlottableType \| str` | `None` | Data type hint: `"quantitative"`, `"nominal"`, or `"temporal"`. Inferred automatically when omitted. |

### Examples

```python
# Simple field reference (same as using the string "sales" directly)
nib.PlottableField("sales")

# Typed temporal field
nib.PlottableField("date", type=nib.PlottableType.TEMPORAL)

# Color encoding by category
nib.LineMark(
    x="date",
    y="value",
    foreground_style=nib.PlottableField("category"),
)
```

---

## PlottableValue

A static value for chart encoding, primarily used with `RuleMark` to create reference lines at fixed positions with optional labels.

### Constructor

```python
nib.PlottableValue(value, label=None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `int \| float \| str` | *required* | The static value. A number for quantitative axes, or a string for categorical axes. |
| `label` | `str` | `None` | Optional label text displayed alongside the value (e.g., `"Target"`, `"Average"`). |

### Examples

```python
# Reference line at a fixed value with label
nib.RuleMark(y=nib.PlottableValue(100, label="Target"))

# Simple numeric value (equivalent shorthand)
nib.RuleMark(y=100)
```

---

## Enumerations

### InterpolationMethod

Curve interpolation methods for `LineMark` and `AreaMark`.

| Value | Description |
|-------|-------------|
| `LINEAR` | Straight lines between points. Default. |
| `MONOTONE` | Smooth curve preserving monotonicity. No artificial peaks between points. |
| `CATMULL_ROM` | Smooth cubic spline through all points. May overshoot. |
| `CARDINAL` | Smooth curve with adjustable tension. |
| `STEP_START` | Horizontal step, transitioning at interval start. |
| `STEP_CENTER` | Horizontal step, transitioning at interval midpoint. |
| `STEP_END` | Horizontal step, transitioning at interval end. |

```python
nib.LineMark(x="date", y="temp", interpolation=nib.InterpolationMethod.MONOTONE)
```

### StackingMethod

Stacking modes for `BarMark` and `AreaMark`.

| Value | Description |
|-------|-------------|
| `STANDARD` | Values stacked on top of each other. Y-axis reflects cumulative total. |
| `NORMALIZED` | Values scaled to 100% at each x position. Shows relative proportions. |
| `CENTER` | Values centered around the middle axis (stream graph effect). |

```python
nib.BarMark(x="q", y="rev", foreground_style=nib.PlottableField("region"),
            stacking=nib.StackingMethod.STANDARD)
```

### SymbolShape

Point marker shapes for `PointMark` and `LineMark`.

| Value | Description |
|-------|-------------|
| `CIRCLE` | Filled circle. Default and most common. |
| `SQUARE` | Filled square. |
| `TRIANGLE` | Filled upward-pointing triangle. |
| `DIAMOND` | Filled diamond (rotated square). |
| `CROSS` | X-shaped cross. Lighter visual weight. |
| `PLUS` | Plus sign. Axis-aligned. |
| `PENTAGON` | Filled five-sided polygon. |
| `HEXAGON` | Filled six-sided polygon. |

```python
nib.PointMark(x="x", y="y", symbol=nib.SymbolShape.DIAMOND, symbol_size=100)
```

### AxisPosition

Axis placement relative to the plot area.

| Value | Description |
|-------|-------------|
| `BOTTOM` | Below the plot area. Default for x-axis. |
| `TOP` | Above the plot area. |
| `LEADING` | Left side (LTR). Default for y-axis. |
| `TRAILING` | Right side (LTR). |

### LegendPosition

Legend placement relative to the chart.

| Value | Description |
|-------|-------------|
| `TOP` | Above the chart. |
| `BOTTOM` | Below the chart. |
| `LEADING` | Left side (LTR). |
| `TRAILING` | Right side (LTR). |
| `AUTOMATIC` | System chooses based on available space. |
| `HIDDEN` | Legend is not displayed. |

### PlottableType

Data type hints for plottable values.

| Value | Description |
|-------|-------------|
| `QUANTITATIVE` | Numeric data on a continuous linear scale. |
| `NOMINAL` | Categorical data with no inherent order. Discrete band scale. |
| `TEMPORAL` | Date/time data. Time-aware scale with intelligent tick formatting. |

```python
nib.PlottableField("date", type=nib.PlottableType.TEMPORAL)
```
