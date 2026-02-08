# RectMark

Draws filled rectangles defined by their bounds in data space. RectMark is ideal for heatmaps, Gantt charts, range visualizations, and other grid-based charts where each cell represents a data value.

Rectangles can be positioned using center points (`x`, `y`) for automatic sizing, or explicit bounds (`x_start`/`x_end`, `y_start`/`y_end`) for precise control.

RectMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.RectMark(
    x=None,
    x_start=None,
    x_end=None,
    y=None,
    y_start=None,
    y_end=None,
    foreground_style=None,
    corner_radius=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| PlottableField` | `None` | Data field for the x-axis center position. Used for categorical grids where cell width is determined automatically. |
| `x_start` | `str \| PlottableField` | `None` | Data field for the left edge of the rectangle. |
| `x_end` | `str \| PlottableField` | `None` | Data field for the right edge of the rectangle. |
| `y` | `str \| PlottableField` | `None` | Data field for the y-axis center position. Used for categorical grids where cell height is determined automatically. |
| `y_start` | `str \| PlottableField` | `None` | Data field for the bottom edge of the rectangle. |
| `y_end` | `str \| PlottableField` | `None` | Data field for the top edge of the rectangle. |
| `foreground_style` | `str \| PlottableField` | `None` | Fill color. Accepts hex strings, named colors, or a `PlottableField` to encode data values as colors (essential for heatmaps). |
| `corner_radius` | `float` | `None` | Radius for rounded corners in points. |
| `opacity` | `float` | `None` | Opacity from 0.0 to 1.0. |

## Examples

### Heatmap

```python
import nib

data = [
    {"weekday": "Mon", "hour": "9am", "intensity": "high"},
    {"weekday": "Mon", "hour": "12pm", "intensity": "medium"},
    {"weekday": "Tue", "hour": "9am", "intensity": "low"},
    {"weekday": "Tue", "hour": "12pm", "intensity": "high"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.RectMark(
            x="weekday",
            y="hour",
            foreground_style=nib.PlottableField("intensity"),
        ),
    ],
    width=300,
    height=200,
)
```

### Gantt chart (range chart)

```python
import nib

tasks = [
    {"task": "Design", "start": 0, "end": 3, "status": "complete"},
    {"task": "Develop", "start": 2, "end": 7, "status": "in-progress"},
    {"task": "Test", "start": 6, "end": 9, "status": "pending"},
]

chart = nib.Chart(
    data=tasks,
    marks=[
        nib.RectMark(
            x_start="start",
            x_end="end",
            y="task",
            foreground_style=nib.PlottableField("status"),
            corner_radius=4,
        ),
    ],
    legend=nib.ChartLegend(position="bottom"),
    width=400,
    height=200,
)
```

### Calendar heatmap cells

```python
import nib

chart = nib.Chart(
    data=calendar_data,
    marks=[
        nib.RectMark(
            x="week",
            y="day_of_week",
            foreground_style=nib.PlottableField("contributions"),
            corner_radius=2,
        ),
    ],
    width=500,
    height=150,
)
```
