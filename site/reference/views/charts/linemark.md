# LineMark

Connects data points with a continuous line, ideal for showing trends over time or continuous relationships between variables. Lines can be styled with different colors, widths, and interpolation methods. Optional symbols (markers) can be placed at each data point for individual value visibility.

LineMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.LineMark(
    x,
    y,
    foreground_style=None,
    symbol=None,
    interpolation=None,
    line_width=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| PlottableField` | *required* | Data field name for the x-axis position. Can be a string or a `PlottableField` with explicit type information. |
| `y` | `str \| PlottableField` | *required* | Data field name for the y-axis position. Can be a string or a `PlottableField` with explicit type information. |
| `foreground_style` | `str \| PlottableField` | `None` | Line color. Accepts hex strings (`"#3B82F6"`), named colors (`"blue"`), or a `PlottableField` to color lines by a data category (automatic palette assignment). |
| `symbol` | `SymbolShape \| str \| PlottableField` | `None` | Shape of data point markers. Use a `SymbolShape` enum (`CIRCLE`, `SQUARE`, `TRIANGLE`, `DIAMOND`, `CROSS`, `PLUS`, `PENTAGON`, `HEXAGON`), a string, or a `PlottableField` to vary symbols by category. |
| `interpolation` | `InterpolationMethod \| str` | `None` | Curve interpolation method between points. Options: `LINEAR` (default), `MONOTONE`, `CATMULL_ROM`, `CARDINAL`, `STEP_START`, `STEP_CENTER`, `STEP_END`. |
| `line_width` | `float` | `None` | Width of the line in points. Uses system default when not specified. |
| `opacity` | `float` | `None` | Opacity from 0.0 (transparent) to 1.0 (opaque). |

## Examples

### Basic line chart

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"month": "Jan", "temp": 5},
            {"month": "Feb", "temp": 7},
            {"month": "Mar", "temp": 12},
            {"month": "Apr", "temp": 17},
        ],
        marks=[nib.LineMark(x="month", y="temp")],
        width=300,
        height=200,
    )
    app.build(chart)

nib.run(main)
```

### Styled line with symbols

```python
import nib

chart = nib.Chart(
    data=monthly_data,
    marks=[
        nib.LineMark(
            x="month",
            y="sales",
            foreground_style="#3B82F6",
            symbol=nib.SymbolShape.CIRCLE,
            line_width=2.0,
            interpolation=nib.InterpolationMethod.MONOTONE,
        ),
    ],
    width=400,
    height=250,
)
```

### Multi-series with color encoding

```python
import nib

data = [
    {"date": "Jan", "value": 10, "series": "A"},
    {"date": "Feb", "value": 20, "series": "A"},
    {"date": "Jan", "value": 15, "series": "B"},
    {"date": "Feb", "value": 25, "series": "B"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.LineMark(
            x="date",
            y="value",
            foreground_style=nib.PlottableField("series"),
        ),
    ],
    width=400,
    height=250,
)
```

### Step chart for discrete events

```python
import nib

chart = nib.Chart(
    data=state_changes,
    marks=[
        nib.LineMark(
            x="time",
            y="state",
            interpolation=nib.InterpolationMethod.STEP_END,
            foreground_style="#F59E0B",
        ),
    ],
    width=400,
    height=200,
)
```
