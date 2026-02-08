# PointMark

Displays individual data points as symbols, ideal for scatter plots and showing relationships between two quantitative variables. Each point can be customized with different shapes, sizes, and colors.

PointMark is commonly used for scatter plots, bubble charts (with size encoding), and adding data point markers to other chart types.

PointMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.PointMark(
    x,
    y,
    foreground_style=None,
    symbol=None,
    symbol_size=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| PlottableField` | *required* | Data field for the x-axis position. |
| `y` | `str \| PlottableField` | *required* | Data field for the y-axis position. |
| `foreground_style` | `str \| PlottableField` | `None` | Point fill color. Accepts hex strings, named colors, or a `PlottableField` to color points by category. |
| `symbol` | `SymbolShape \| str \| PlottableField` | `None` | Shape of the point marker. Use a `SymbolShape` enum (`CIRCLE`, `SQUARE`, `TRIANGLE`, `DIAMOND`, `CROSS`, `PLUS`, `PENTAGON`, `HEXAGON`), a string, or a `PlottableField` to vary symbols by data category. |
| `symbol_size` | `float` | `None` | Size of the symbol in square points. Larger values create bigger markers. Uses system default when not specified. |
| `opacity` | `float` | `None` | Opacity from 0.0 to 1.0. Useful for dense scatter plots where points overlap. |

## Examples

### Basic scatter plot

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"height": 165, "weight": 60},
            {"height": 170, "weight": 72},
            {"height": 175, "weight": 80},
            {"height": 180, "weight": 85},
            {"height": 160, "weight": 55},
        ],
        marks=[nib.PointMark(x="height", y="weight")],
        x_axis=nib.ChartAxis(label="Height (cm)"),
        y_axis=nib.ChartAxis(label="Weight (kg)"),
        width=300,
        height=250,
    )
    app.build(chart)

nib.run(main)
```

### Colored by category

```python
import nib

data = [
    {"x": 5.1, "y": 3.5, "species": "Setosa"},
    {"x": 7.0, "y": 3.2, "species": "Versicolor"},
    {"x": 6.3, "y": 3.3, "species": "Virginica"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.PointMark(
            x="x",
            y="y",
            foreground_style=nib.PlottableField("species"),
        ),
    ],
    legend=nib.ChartLegend(position="bottom"),
    width=400,
    height=300,
)
```

### Custom symbols and size

```python
import nib

chart = nib.Chart(
    data=measurements,
    marks=[
        nib.PointMark(
            x="x",
            y="y",
            symbol=nib.SymbolShape.DIAMOND,
            symbol_size=100,
            foreground_style="#EF4444",
        ),
    ],
    width=350,
    height=250,
)
```

### Symbols varying by data

```python
import nib

chart = nib.Chart(
    data=multi_category_data,
    marks=[
        nib.PointMark(
            x="x",
            y="y",
            symbol=nib.PlottableField("category"),
            foreground_style=nib.PlottableField("category"),
        ),
    ],
    width=400,
    height=300,
)
```
