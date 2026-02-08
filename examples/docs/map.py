import nib


def main(app: nib.App):
    app.title = "Map"
    app.icon = nib.SFSymbol("map")
    app.width = 400
    app.height = 450

    app.build(
        nib.VStack(
            controls=[
                nib.Text("San Francisco", font=nib.Font.HEADLINE),
                nib.Map(
                    latitude=37.7749,
                    longitude=-122.4194,
                    zoom=0.05,
                    markers=[
                        nib.MapMarker(37.7749, -122.4194, title="San Francisco", tint=nib.Color.RED),
                        nib.MapMarker(37.8199, -122.4783, title="Golden Gate Bridge", tint=nib.Color.ORANGE),
                        nib.MapMarker(37.7694, -122.4862, title="Golden Gate Park", tint=nib.Color.GREEN),
                    ],
                    shows_compass=True,
                    shows_scale=True,
                    height=350,
                ),
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
