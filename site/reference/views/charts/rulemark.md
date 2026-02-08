# RuleMark

Draws straight reference lines across the chart. Rules are useful for showing thresholds, averages, targets, or event markers. They can be horizontal (fixed y, spanning x) or vertical (fixed x, spanning y), and optionally bounded to create line segments.

Values can be static numbers or data field references. When a field name is provided, one rule is drawn per data row.

RuleMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.RuleMark(
    x=None,
    x_start=None,
    x_end=None,
    y=None,
    y_start=None,
    y_end=None,
    foreground_style=None,
    line_width=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| float \| PlottableField \| PlottableValue` | `None` | X-axis position for a vertical rule. Can be a static number, a field name, `PlottableField`, or `PlottableValue`. |
| `x_start` | `str \| float \| PlottableField \| PlottableValue` | `None` | Starting x position for a bounded horizontal rule segment. |
| `x_end` | `str \| float \| PlottableField \| PlottableValue` | `None` | Ending x position for a bounded horizontal rule segment. |
| `y` | `str \| float \| PlottableField \| PlottableValue` | `None` | Y-axis position for a horizontal rule. Can be a static number, a field name, `PlottableField`, or `PlottableValue`. |
| `y_start` | `str \| float \| PlottableField \| PlottableValue` | `None` | Starting y position for a bounded vertical rule segment. |
| `y_end` | `str \| float \| PlottableField \| PlottableValue` | `None` | Ending y position for a bounded vertical rule segment. |
| `foreground_style` | `str \| PlottableField` | `None` | Line color. Accepts hex strings, named colors, or a `PlottableField`. |
| `line_width` | `float` | `None` | Width of the rule line in points. |
| `opacity` | `float` | `None` | Opacity from 0.0 to 1.0. |

## Examples

### Horizontal reference line (target)

```python
import nib

chart = nib.Chart(
    data=[
        {"month": "Jan", "sales": 80},
        {"month": "Feb", "sales": 120},
        {"month": "Mar", "sales": 95},
    ],
    marks=[
        nib.BarMark(x="month", y="sales", foreground_style="#3B82F6"),
        nib.RuleMark(y=100, foreground_style="#EF4444", line_width=2),
    ],
    width=350,
    height=200,
)
```

### Vertical reference line (event marker)

```python
import nib

chart = nib.Chart(
    data=time_series_data,
    marks=[
        nib.LineMark(x="date", y="value"),
        nib.RuleMark(x="2024-06-15", foreground_style="#6366F1"),
    ],
    width=400,
    height=250,
)
```

### Bounded horizontal segment

```python
import nib

chart = nib.Chart(
    data=monthly_data,
    marks=[
        nib.LineMark(x="month", y="value"),
        nib.RuleMark(
            y=50,
            x_start="Jan",
            x_end="Jun",
            foreground_style="#10B981",
            line_width=1.5,
        ),
    ],
    width=400,
    height=200,
)
```

### Labeled reference line with PlottableValue

```python
import nib

chart = nib.Chart(
    data=sales_data,
    marks=[
        nib.BarMark(x="month", y="sales"),
        nib.RuleMark(
            y=nib.PlottableValue(100, label="Target"),
            foreground_style="#F59E0B",
            line_width=1.5,
        ),
    ],
    width=400,
    height=250,
)
```
