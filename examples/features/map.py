import nib


def main(app: nib.App):
    app.title = "Map Demo"
    app.width = 400
    app.height = 400

    app.build(
        nib.Map(
            latitude=37.7749,
            longitude=-122.4194,
            zoom=0.05,
            markers=[
                nib.MapMarker(
                    latitude=37.8044,
                    longitude=-122.2712,
                    title="Oakland",
                    system_image="star.fill",
                ),
            ],
            annotations=[
                nib.MapAnnotation(
                    latitude=37.7749,
                    longitude=-122.4194,
                    content=nib.VStack(
                        controls=[
                            nib.Text("This is the title", style=nib.TextStyle.HEADLINE),
                            nib.Text(
                                "This is the subtitle", style=nib.TextStyle.SUBHEADLINE
                            ),
                        ],
                        padding=4,
                        background=nib.RoundedRectangle(
                            fill=nib.Color.BLACK.with_opacity(0.4),
                            corner_radius=8,
                            opacity=0.8,
                        ),
                    ),
                )
            ],
            polylines=[
                nib.MapPolyline(
                    coordinates=[
                        (37.7749, -122.4194),  # SF
                        (37.8044, -122.2712),  # Oakland
                        (37.8716, -122.2727),  # Berkeley
                    ],
                    stroke=nib.Color.RED,
                    stroke_width=3,
                ),
            ],
            polygons=[
                nib.MapPolygon(
                    coordinates=[
                        (37.78, -122.42),
                        (37.77, -122.40),
                        (37.76, -122.42),
                        (37.77, -122.44),
                    ],
                    fill=nib.Color.GREEN.with_opacity(0.3),
                    stroke=nib.Color.GREEN,
                    stroke_width=2,
                ),
            ],
            circles=[
                nib.MapCircle(
                    latitude=37.7749,
                    longitude=-122.4194,
                    radius=2000,  # 2km
                    fill=nib.Color.BLUE.with_opacity(0.2),
                    stroke=nib.Color.BLUE,
                    stroke_width=2,
                ),
            ],
            style=nib.MapStyle.STANDARD,
            shows_compass=True,
            shows_scale=True,
            corner_radius=12,
        )
    )


nib.run(main)
