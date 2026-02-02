"""Settings test with multiple tabs."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Tabs"
    app.width = 300
    app.height = 200

    # Settings page with multiple tabs
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
            nib.SettingsTab(
                "Account",
                icon="person",
                content=nib.VStack(
                    controls=[
                        nib.Text("Account Settings", font=nib.Font.headline),
                        nib.TextField("Username", value="guest"),
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
                nib.Text("Settings Tabs Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
