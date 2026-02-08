# Charts

Chart views provide data visualization powered by Swift Charts. The `Chart` container renders one or more mark types against a shared dataset, with optional axis and legend configuration.

All chart marks accept data field references as strings (e.g., `x="month"`) or typed `PlottableField` objects for explicit data type hints. Colors can be static (hex strings, named colors) or data-driven via `PlottableField` for automatic palette assignment.

## Container

| View | Description |
|------|-------------|
| [Chart](chart.md) | The main container that holds data, marks, axes, and legend configuration. |

## Marks

| View | Description |
|------|-------------|
| [LineMark](linemark.md) | Connects data points with a continuous line. Supports symbols and interpolation. |
| [BarMark](barmark.md) | Displays data as rectangular bars with stacking and grouping support. |
| [AreaMark](areamark.md) | Fills the region between a line and a baseline for cumulative visualizations. |
| [PointMark](pointmark.md) | Renders individual data points as symbols for scatter plots. |
| [RuleMark](rulemark.md) | Draws reference lines (horizontal or vertical) across the chart. |
| [RectMark](rectmark.md) | Draws filled rectangles for heatmaps, Gantt charts, and range visualizations. |
| [SectorMark](sectormark.md) | Creates pie and donut chart segments from angular data. |

## Configuration

| Class | Description |
|-------|-------------|
| [ChartAxis & ChartLegend](axis-legend.md) | Axis and legend configuration, plus supporting types like `PlottableField`, `InterpolationMethod`, `StackingMethod`, and `SymbolShape`. |

## Quick example

```python
import nib

def main(app: nib.App):
    chart = nib.Chart(
        data=[
            {"month": "Jan", "sales": 100},
            {"month": "Feb", "sales": 150},
            {"month": "Mar", "sales": 200},
            {"month": "Apr", "sales": 180},
        ],
        marks=[nib.LineMark(x="month", y="sales", foreground_style="#3B82F6")],
        x_axis=nib.ChartAxis(label="Month"),
        y_axis=nib.ChartAxis(label="Sales", grid_lines=True),
        width=350,
        height=250,
        padding=16,
    )

    app.build(chart)

nib.run(main)
```
