import random

import nib


def main(app: nib.App):
    # Chart data - more points for smoother curve
    data = [
        {"x": 0, "y": 4},
        {"x": 1, "y": 6},
        {"x": 2, "y": 12},
        {"x": 3, "y": 14},
        {"x": 4, "y": 10},
        {"x": 5, "y": 8},
        {"x": 6, "y": 11},
        {"x": 7, "y": 9},
    ]

    gradient = nib.LinearGradient(
        colors=[nib.Color.WHITE, nib.Color.GRAY.with_opacity(0.2)],
        start=(1, 0),
        end=(1, 1),
    )

    # Create a mini sparkline as the status bar icon
    chart = nib.Chart(
        data=data,
        marks=[
            nib.AreaMark(
                x="x",
                y="y",
                foreground_style=gradient,
                interpolation=nib.InterpolationMethod.CATMULL_ROM,
            ),
            nib.LineMark(
                x="x",
                y="y",
                foreground_style="#ffffff",
                line_width=1.0,
                interpolation=nib.InterpolationMethod.CATMULL_ROM,
            ),
        ],
        x_axis=nib.ChartAxis(hidden=True),
        y_axis=nib.ChartAxis(hidden=True),
        legend=nib.ChartLegend(hidden=True),
        width=30,
        height=16,
    )

    app.icon = chart

    def randomize():
        chart.data = [{"x": i, "y": random.randint(4, 16)} for i in range(8)]

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Chart Icon Demo", font=nib.Font.HEADLINE),
                nib.Text("The status bar shows a mini chart"),
                nib.Button("Randomize", action=randomize),
            ],
            spacing=12,
            padding=20,
            width=250,
        )
    )


nib.run(main)
