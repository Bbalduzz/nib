import nib


def main(app: nib.App):
    app.title = "Usage"
    app.icon = nib.SFSymbol("chart.bar.fill")
    app.width = 400
    app.height = 500

    # Data with series column for grouping
    data = [
        # Subscription (blue bars)
        {"date": "10/23", "value": 74, "series": "Subscription"},
        {"date": "10/24", "value": 54, "series": "Subscription"},
        {"date": "10/27", "value": 0, "series": "Subscription"},
        {"date": "10/28", "value": 0, "series": "Subscription"},
        {"date": "10/29", "value": 0, "series": "Subscription"},
        {"date": "10/30", "value": 0, "series": "Subscription"},
        # Usage Based (orange bars)
        {"date": "10/23", "value": 0, "series": "Usage Based"},
        {"date": "10/24", "value": 0, "series": "Usage Based"},
        {"date": "10/27", "value": 35, "series": "Usage Based"},
        {"date": "10/28", "value": 30, "series": "Usage Based"},
        {"date": "10/29", "value": 45, "series": "Usage Based"},
        {"date": "10/30", "value": 6, "series": "Usage Based"},
    ]

    chart = nib.Chart(
        data=data,
        marks=[
            nib.BarMark(
                x="date",
                y="value",
                foreground_style=nib.PlottableField("series"),  # Groups by series
                corner_radius=4,
            ),
        ],
        x_axis=nib.ChartAxis(label=None),
        y_axis=nib.ChartAxis(label=None),
        legend=nib.ChartLegend(position="bottom"),
        # chart_background="#2d2d2d",
        width=360,
        height=280,
    )

    # Calculate stats
    values = [d["value"] for d in data if d["value"] > 0]
    total = sum(values)
    average = round(total / len(values), 1) if values else 0
    peak = max(values) if values else 0

    app.build(
        nib.VStack(
            controls=[
                # Header
                nib.HStack(
                    controls=[
                        nib.Text("Usage", font=nib.Font.title2),
                        nib.SFSymbol("chevron.down", foreground_color="#888"),
                    ],
                    spacing=4,
                ),
                # Chart
                chart,
                # Stats row
                nib.HStack(
                    controls=[
                        nib.VStack(
                            controls=[
                                nib.Text(
                                    "Total",
                                    font=nib.Font.caption,
                                    foreground_color="#888",
                                ),
                                nib.Text(str(total), font=nib.Font.title),
                            ],
                            alignment="leading",
                        ),
                        nib.VStack(
                            controls=[
                                nib.Text(
                                    "Average",
                                    font=nib.Font.caption,
                                    foreground_color="#888",
                                ),
                                nib.Text(str(average), font=nib.Font.title),
                            ],
                            alignment="leading",
                        ),
                        nib.VStack(
                            controls=[
                                nib.Text(
                                    "Peak",
                                    font=nib.Font.caption,
                                    foreground_color="#888",
                                ),
                                nib.Text(str(peak), font=nib.Font.title),
                            ],
                            alignment="leading",
                        ),
                    ],
                    spacing=40,
                ),
            ],
            spacing=16,
            padding=20,
        )
    )


nib.run(main)
