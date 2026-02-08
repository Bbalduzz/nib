import nib


def main(app: nib.App):
    app.title = "ShareLink"
    app.icon = nib.SFSymbol("square.and.arrow.up")
    app.width = 300
    app.height = 200

    app.build(
        nib.VStack(
            controls=[
                nib.ShareLink(
                    items=["Check out this app!"],
                    label="Share Text",
                ),
                nib.ShareLink(
                    items=["https://example.com"],
                    label="Share URL",
                    icon="link",
                    subject="Cool Website",
                    message="Take a look at this!",
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
