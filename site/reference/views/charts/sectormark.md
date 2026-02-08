# SectorMark

Creates circular segments (wedges) based on angular data, suited for pie and donut charts showing proportional relationships and part-to-whole comparisons. Setting `inner_radius` to a value greater than zero creates a donut chart instead of a pie chart.

The `angle` field determines the size of each sector proportionally. Use `foreground_style` with a `PlottableField` to automatically assign colors to each category.

SectorMark is used inside a `Chart` container as one of the `marks` entries.

## Constructor

```python
nib.SectorMark(
    angle,
    foreground_style=None,
    inner_radius=None,
    outer_radius=None,
    angle_start=None,
    corner_radius=None,
    opacity=None,
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `angle` | `str \| PlottableField` | *required* | Data field containing values that determine sector sizes. Values are treated proportionally -- a sector with value 20 is twice as large as one with value 10. |
| `foreground_style` | `str \| PlottableField` | `None` | Fill color for sectors. Use a `PlottableField` with a categorical field to automatically assign different colors to each sector. |
| `inner_radius` | `float` | `None` | Inner radius in points. Set to `0` (or omit) for a pie chart. Set to a positive value for a donut chart. |
| `outer_radius` | `float` | `None` | Outer radius in points. Defaults to automatic sizing based on available space. |
| `angle_start` | `str \| PlottableField` | `None` | Data field or value for the starting angle of sectors. Rarely needed; use for custom sector positioning. |
| `corner_radius` | `float` | `None` | Radius for rounded sector corners in points. Creates a softer visual appearance. |
| `opacity` | `float` | `None` | Opacity from 0.0 to 1.0. |

## Examples

### Pie chart

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"category": "Electronics", "value": 42},
            {"category": "Clothing", "value": 28},
            {"category": "Food", "value": 20},
            {"category": "Books", "value": 10},
        ],
        marks=[
            nib.SectorMark(
                angle="value",
                foreground_style=nib.PlottableField("category"),
            ),
        ],
        legend=nib.ChartLegend(position="bottom"),
        width=300,
        height=300,
    )
    app.build(chart)

nib.run(main)
```

### Donut chart

```python
import nib

chart = nib.Chart(
    data=[
        {"segment": "Used", "percentage": 65},
        {"segment": "Free", "percentage": 35},
    ],
    marks=[
        nib.SectorMark(
            angle="percentage",
            foreground_style=nib.PlottableField("segment"),
            inner_radius=50,
            outer_radius=100,
        ),
    ],
    width=250,
    height=250,
)
```

### Styled donut with rounded segments

```python
import nib

chart = nib.Chart(
    data=[
        {"region": "North", "sales": 120},
        {"region": "South", "sales": 90},
        {"region": "East", "sales": 75},
        {"region": "West", "sales": 110},
    ],
    marks=[
        nib.SectorMark(
            angle="sales",
            foreground_style=nib.PlottableField("region"),
            inner_radius=40,
            outer_radius=80,
            corner_radius=4,
        ),
    ],
    legend=nib.ChartLegend(position="trailing", title="Region"),
    width=300,
    height=300,
    padding=16,
)
```
