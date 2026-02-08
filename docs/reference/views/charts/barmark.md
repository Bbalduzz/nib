# BarMark

Displays data as rectangular bars, ideal for comparing discrete categories or showing distributions. Bars can be oriented vertically or horizontally and support stacking for multi-series comparisons.

The orientation is determined by which fields are categorical versus quantitative. For vertical bars, `x` is typically categorical and `y` is quantitative. Swap the fields for horizontal bars.

BarMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.BarMark(
    x=None,
    y=None,
    width=None,
    height=None,
    foreground_style=None,
    stacking=None,
    corner_radius=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | `str \| PlottableField` | `None` | Data field for the x-axis. For vertical bars, this is typically the categorical field. |
| `y` | `str \| PlottableField` | `None` | Data field for the y-axis. For vertical bars, this is the quantitative field (bar height). |
| `width` | `float` | `None` | Fixed bar width in points. If not specified, bars are sized automatically. |
| `height` | `float` | `None` | Fixed bar height in points. If not specified, bars are sized by y data values. |
| `foreground_style` | `str \| PlottableField` | `None` | Bar fill color. Accepts hex strings, named colors, or a `PlottableField` to color bars by category (creates grouped or stacked bars). |
| `stacking` | `StackingMethod \| str` | `None` | How to stack bars when multiple series overlap. Options: `STANDARD` (stacked), `NORMALIZED` (100% stacked), `CENTER` (centered). Default is no stacking (bars are grouped side by side). |
| `corner_radius` | `float` | `None` | Radius for rounded bar corners in points. |
| `opacity` | `float` | `None` | Opacity from 0.0 to 1.0. |

## Examples

### Simple vertical bar chart

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"product": "A", "sales": 120},
            {"product": "B", "sales": 200},
            {"product": "C", "sales": 150},
        ],
        marks=[nib.BarMark(x="product", y="sales", foreground_style="#10B981")],
        width=300,
        height=200,
    )
    app.build(chart)

nib.run(main)
```

### Horizontal bar chart

```python
import nib

chart = nib.Chart(
    data=[
        {"lang": "Python", "users": 45},
        {"lang": "JavaScript", "users": 38},
        {"lang": "Rust", "users": 12},
    ],
    marks=[nib.BarMark(x="users", y="lang")],
    width=350,
    height=200,
)
```

### Stacked bar chart

```python
import nib

data = [
    {"quarter": "Q1", "revenue": 100, "region": "US"},
    {"quarter": "Q1", "revenue": 80, "region": "EU"},
    {"quarter": "Q2", "revenue": 120, "region": "US"},
    {"quarter": "Q2", "revenue": 90, "region": "EU"},
]

chart = nib.Chart(
    data=data,
    marks=[
        nib.BarMark(
            x="quarter",
            y="revenue",
            foreground_style=nib.PlottableField("region"),
            stacking=nib.StackingMethod.STANDARD,
        ),
    ],
    legend=nib.ChartLegend(position="bottom"),
    width=400,
    height=250,
)
```

### Styled bars with rounded corners

```python
import nib

chart = nib.Chart(
    data=product_data,
    marks=[
        nib.BarMark(
            x="product",
            y="revenue",
            foreground_style="#8B5CF6",
            corner_radius=4,
        ),
    ],
    width=300,
    height=200,
)
```
