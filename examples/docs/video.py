import nib


def main(app: nib.App):
    app.title = "Video"
    app.icon = nib.SFSymbol("play.rectangle")
    app.width = 400
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Video Player", font=nib.Font.HEADLINE),
                nib.Video(
                    src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                    autoplay=False,
                    controls=True,
                    loop=False,
                    height=250,
                    corner_radius=8,
                ),
            ],
            spacing=8,
            padding=20,
        )
    )


nib.run(main)
