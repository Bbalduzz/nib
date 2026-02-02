"""Settings test with VStack content."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings VStack"
    app.width = 300
    app.height = 200

    # Settings page with VStack content
    app.settings = nib.SettingsPage(
        title="Preferences",
        width=400,
        height=300,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.VStack(
                    controls=[
                        nib.Text("General Settings", font=nib.Font.headline),
                        nib.Text("Some description text"),
                    ],
                    spacing=12,
                    padding=20,
                ),
            ),
        ],
    )

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Settings VStack Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
