"""
Nib Charts Demo - Swift Charts integration showcase

Demonstrates various chart types:
- Line charts
- Bar charts
- Area charts
- Point/scatter charts
- Pie/donut charts (SectorMark)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))
import nib


def main(app: nib.App):
    app.title = "Charts"
    app.icon = nib.SFSymbol("chart.bar.fill")
    app.width = 400
    app.height = 600

    # Sample data for line/bar/area charts
    monthly_sales = [
        {"month": "Jan", "sales": 120, "region": "East"},
        {"month": "Feb", "sales": 150, "region": "East"},
        {"month": "Mar", "sales": 180, "region": "East"},
        {"month": "Apr", "sales": 140, "region": "East"},
        {"month": "May", "sales": 200, "region": "East"},
        {"month": "Jun", "sales": 170, "region": "East"},
        {"month": "Jan", "sales": 80, "region": "West"},
        {"month": "Feb", "sales": 100, "region": "West"},
        {"month": "Mar", "sales": 130, "region": "West"},
        {"month": "Apr", "sales": 90, "region": "West"},
        {"month": "May", "sales": 160, "region": "West"},
        {"month": "Jun", "sales": 120, "region": "West"},
    ]

    # Sample data for pie chart
    market_share = [
        {"product": "Product A", "share": 35},
        {"product": "Product B", "share": 25},
        {"product": "Product C", "share": 20},
        {"product": "Product D", "share": 15},
        {"product": "Other", "share": 5},
    ]

    # Simple bar data
    simple_data = [
        {"category": "A", "value": 50},
        {"category": "B", "value": 80},
        {"category": "C", "value": 60},
        {"category": "D", "value": 90},
    ]

    # Current chart index
    chart_index = {"value": 0}
    chart_names = [
        "Line Chart",
        "Bar Chart",
        "Area Chart",
        "Scatter Plot",
        "Pie Chart",
        "Donut Chart",
    ]

    # Chart container that will be updated
    chart_container = nib.VStack(controls=[], padding=16)

    def update_chart():
        idx = chart_index["value"]
        if idx == 0:
            # Line chart with multiple series
            chart_container._children = [
                nib.Text("Multi-Series Line Chart", font=nib.Font.headline),
                nib.Chart(
                    data=monthly_sales,
                    marks=[
                        nib.LineMark(
                            x="month",
                            y="sales",
                            foreground_style="region",
                            interpolation=nib.InterpolationMethod.CATMULL_ROM,
                            line_width=2,
                        ),
                        nib.PointMark(
                            x="month",
                            y="sales",
                            foreground_style="region",
                            symbol_size=50,
                        ),
                    ],
                    x_axis=nib.ChartAxis(label="Month"),
                    y_axis=nib.ChartAxis(label="Sales ($)", grid_lines=True),
                    width=350,
                    height=250,
                ),
            ]
        elif idx == 1:
            # Bar chart
            chart_container._children = [
                nib.Text("Simple Bar Chart", font=nib.Font.headline),
                nib.Chart(
                    data=simple_data,
                    marks=[
                        nib.BarMark(
                            x="category",
                            y="value",
                            foreground_style="category",
                            corner_radius=4,
                        ),
                    ],
                    x_axis=nib.ChartAxis(label="Category"),
                    y_axis=nib.ChartAxis(label="Value", grid_lines=True),
                    width=350,
                    height=250,
                ),
            ]
        elif idx == 2:
            # Area chart
            chart_container._children = [
                nib.Text("Area Chart", font=nib.Font.headline),
                nib.Chart(
                    data=monthly_sales,
                    marks=[
                        nib.AreaMark(
                            x="month",
                            y="sales",
                            foreground_style="region",
                            interpolation=nib.InterpolationMethod.MONOTONE,
                            opacity=0.5,
                        ),
                    ],
                    x_axis=nib.ChartAxis(label="Month"),
                    y_axis=nib.ChartAxis(label="Sales ($)", grid_lines=True),
                    width=350,
                    height=250,
                ),
            ]
        elif idx == 3:
            # Scatter plot
            scatter_data = [
                {"x": "A", "y": 10, "size": 100},
                {"x": "B", "y": 25, "size": 150},
                {"x": "C", "y": 15, "size": 80},
                {"x": "D", "y": 30, "size": 200},
                {"x": "E", "y": 20, "size": 120},
            ]
            chart_container._children = [
                nib.Text("Scatter Plot", font=nib.Font.headline),
                nib.Chart(
                    data=scatter_data,
                    marks=[
                        nib.PointMark(
                            x="x",
                            y="y",
                            foreground_style="x",
                            symbol_size=150,
                        ),
                    ],
                    x_axis=nib.ChartAxis(label="Category"),
                    y_axis=nib.ChartAxis(label="Value", grid_lines=True),
                    width=350,
                    height=250,
                ),
            ]
        elif idx == 4:
            # Pie chart
            chart_container._children = [
                nib.Text("Pie Chart", font=nib.Font.headline),
                nib.Chart(
                    data=market_share,
                    marks=[
                        nib.SectorMark(
                            angle="share",
                            foreground_style="product",
                        ),
                    ],
                    legend=nib.ChartLegend(position="bottom"),
                    width=350,
                    height=300,
                ),
            ]
        elif idx == 5:
            # Donut chart
            chart_container._children = [
                nib.Text("Donut Chart", font=nib.Font.headline),
                nib.Chart(
                    data=market_share,
                    marks=[
                        nib.SectorMark(
                            angle="share",
                            foreground_style="product",
                            inner_radius=0.5,
                            corner_radius=4,
                        ),
                    ],
                    legend=nib.ChartLegend(position="bottom"),
                    width=350,
                    height=300,
                ),
            ]
        chart_container._trigger_update()

    def prev_chart():
        chart_index["value"] = (chart_index["value"] - 1) % len(chart_names)
        update_chart()

    def next_chart():
        chart_index["value"] = (chart_index["value"] + 1) % len(chart_names)
        update_chart()

    # Initialize first chart
    update_chart()

    # Navigation buttons
    nav_buttons = nib.HStack(
        controls=[
            nib.Button(
                "Previous",
                action=prev_chart,
                style=nib.ButtonStyle.bordered,
            ),
            nib.Spacer(),
            nib.Button(
                "Next",
                action=next_chart,
                style=nib.ButtonStyle.bordered,
            ),
        ],
        padding={"horizontal": 16},
    )

    app.build(
        nib.VStack(
            controls=[
                nib.Text(
                    "Nib Charts Demo",
                    font=nib.Font.title,
                    padding={"top": 16, "bottom": 8},
                ),
                nib.Divider(),
                chart_container,
                nib.Spacer(),
                nav_buttons,
            ],
            spacing=8,
            padding={"bottom": 16},
        )
    )


if __name__ == "__main__":
    nib.run(main)
