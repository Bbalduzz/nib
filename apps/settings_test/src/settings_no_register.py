"""Settings test - Settings object created but NOT registered."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings No Register"
    app.width = 300
    app.height = 200

    # Create settings but DON'T register
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
    })
    # NOT calling: app.register_settings(settings)

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
                nib.Text("Settings No Register Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
