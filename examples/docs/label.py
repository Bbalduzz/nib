import nib


def main(app: nib.App):
    app.title = "Label"
    app.icon = nib.SFSymbol("tag")
    app.width = 300
    app.height = 300

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Labels", font=nib.Font.HEADLINE),
                nib.Label("Settings", icon="gear"),
                nib.Label("Favorites", icon="star.fill"),
                nib.Label("Trash", icon="trash"),
                nib.Label("Downloads", icon="arrow.down.circle"),
                nib.Divider(),
                nib.Text("Styles", font=nib.Font.HEADLINE),
                nib.Label("Title Only", icon="eye", style=nib.LabelStyle.TITLE_ONLY),
                nib.Label("Icon Only", icon="eye", style=nib.LabelStyle.ICON_ONLY),
                nib.Label("Title and Icon", icon="eye", style=nib.LabelStyle.TITLE_AND_ICON),
            ],
            spacing=8,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
