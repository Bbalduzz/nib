import nib


def main(app: nib.App):
    app.title = "Link"
    app.icon = nib.SFSymbol("link")
    app.width = 300
    app.height = 200

    app.build(
        nib.VStack(
            controls=[
                nib.Link("Visit Apple", url="https://apple.com"),
                nib.Link("Send Email", url="mailto:hello@example.com"),
                nib.Link(
                    url="https://github.com",
                    content=nib.HStack(
                        controls=[
                            nib.Label("GitHub", icon="chevron.left.forwardslash.chevron.right"),
                        ],
                    ),
                ),
            ],
            spacing=12,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
