import nib


def main(app: nib.App):
    app.title = "CameraPreview"
    app.icon = nib.SFSymbol("camera")
    app.width = 350
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Camera", font=nib.Font.HEADLINE),
                nib.CameraPreview(
                    width=300,
                    height=250,
                    corner_radius=12,
                ),
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
