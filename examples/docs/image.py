import nib


def main(app: nib.App):
    app.title = "Image"
    app.icon = nib.SFSymbol("photo")
    app.width = 300
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.Text("From URL", font=nib.Font.HEADLINE),
                nib.Image(
                    src="https://picsum.photos/200/120",
                    width=200,
                    height=120,
                    corner_radius=8,
                ),
                nib.Divider(),
                nib.Text("Clipped to circle", font=nib.Font.HEADLINE),
                nib.Image(
                    src="https://picsum.photos/100/100",
                    width=80,
                    height=80,
                    clip_shape="circle",
                ),
                nib.Divider(),
                nib.Text("With aspect ratio", font=nib.Font.HEADLINE),
                nib.Image(
                    src="https://picsum.photos/300/200",
                    width=250,
                    height=100,
                    aspect_ratio=nib.ContentMode.FILL,
                    corner_radius=8,
                    clip_shape=nib.Rectangle(corner_radius=8),
                ),
            ],
            spacing=10,
            padding=20,
        )
    )


nib.run(main)
