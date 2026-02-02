"""Settings test with Settings class."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Class"
    app.width = 300
    app.height = 200

    # Create settings with defaults
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
    })
    app.register_settings(settings)

    # Settings page
    app.settings = nib.SettingsPage(
        title="Preferences",
        width=450,
        height=350,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.VStack(
                    controls=[
                        nib.Text("General Settings", font=nib.Font.headline),
                        nib.Toggle("Dark Mode", is_on=False),
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
                nib.Text("Settings Class Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
