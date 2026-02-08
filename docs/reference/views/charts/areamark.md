# AreaMark

Fills the region between a line and a baseline, creating a visual representation of cumulative values or ranges. Area charts are effective for showing magnitude over time, and they support stacking for multi-series data.

By default, the area extends from zero to the y value. Use `y_start` to create range areas or band charts.

AreaMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.AreaMark(
    x,
    y,
    y_start=None,
    foreground_style=None,
    interpolation=None,
    stacking=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| PlottableField` | *required* | Data field for the x-axis position. |
| `y` | `str \| PlottableField` | *required* | Data field for the upper boundary of the area (y-axis). |
| `y_start` | `str \| PlottableField` | `None` | Data field for the lower boundary of the area. If omitted, the area extends from zero to the y value. Use this for range or band visualizations. |
| `foreground_style` | `str \| PlottableField` | `None` | Fill color. Accepts hex strings, named colors, or a `PlottableField` for multi-series coloring with automatic palette assignment. |
| `interpolation` | `InterpolationMethod \| str` | `None` | Curve interpolation method. Options: `LINEAR`, `MONOTONE`, `CATMULL_ROM`, `CARDINAL`, `STEP_START`, `STEP_CENTER`, `STEP_END`. |
| `stacking` | `StackingMethod \| str` | `None` | Stacking mode for multi-series areas. Options: `STANDARD` (stacked), `NORMALIZED` (100% stacked), `CENTER` (stream graph). |
| `opacity` | `float` | `None` | Fill opacity from 0.0 to 1.0. Consider lower values (0.3--0.7) for overlapping areas. |

## Examples

### Basic area chart

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"date": "Jan", "revenue": 100},
            {"date": "Feb", "revenue": 150},
            {"date": "Mar", "revenue": 200},
            {"date": "Apr", "revenue": 180},
        ],
        marks=[
            nib.AreaMark(x="date", y="revenue", foreground_style="#3B82F6", opacity=0.5),
        ],
        width=350,
        height=200,
    )
    app.build(chart)

nib.run(main)
```

### Stacked area chart

```python
import nib

data = [
    {"month": "Jan", "value": 30, "category": "A"},
    {"month": "Jan", "value": 20, "category": "B"},
    {"month": "Feb", "value": 35, "category": "A"},
    {"month": "Feb", "value": 25, "category": "B"},
    {"month": "Mar", "value": 40, "category": "A"},
    {"month": "Mar", "value": 30, "category": "B"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.AreaMark(
            x="month",
            y="value",
            foreground_style=nib.PlottableField("category"),
            stacking=nib.StackingMethod.STANDARD,
        ),
    ],
    legend=nib.ChartLegend(position="bottom"),
    width=400,
    height=250,
)
```

### Range/band area

```python
import nib

chart = nib.Chart(
    data=[
        {"date": "Jan", "high": 15, "low": 2},
        {"date": "Feb", "high": 18, "low": 5},
        {"date": "Mar", "high": 22, "low": 10},
    ],
    marks=[
        nib.AreaMark(
            x="date",
            y="high",
            y_start="low",
            foreground_style="#3B82F6",
            opacity=0.3,
        ),
    ],
    width=350,
    height=200,
)
```

### Smooth area with interpolation

```python
import nib

chart = nib.Chart(
    data=time_series,
    marks=[
        nib.AreaMark(
            x="date",
            y="value",
            foreground_style="#8B5CF6",
            interpolation=nib.InterpolationMethod.MONOTONE,
            opacity=0.4,
        ),
    ],
    width=400,
    height=200,
)
```
