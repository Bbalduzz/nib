import nib


def main(app: nib.App):
    app.title = "Menu"
    app.icon = nib.SFSymbol("contextualmenu.and.cursorarrow")
    app.width = 300
    app.height = 150

    app.menu = [
        nib.MenuItem("Preferences", icon="gear", shortcut="cmd+,"),
        nib.MenuItem(
            "More Options",
            menu=[
                nib.MenuItem("Option A", badge="3"),
                nib.MenuItem("Option B", shortcut="cmd+R"),
            ],
        ),
        nib.MenuDivider(),
        nib.MenuItem(
            "Quit",
            icon="power",
            shortcut="cmd+Q",
            action=app.quit,
        ),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Right-click the status bar icon", font=nib.Font.HEADLINE),
                nib.Text(
                    "to see the context menu.",
                    font=nib.Font.CAPTION,
                    foreground_color=nib.Color.SECONDARY,
                ),
            ],
            spacing=4,
            padding=20,
        )
    )


nib.run(main)
