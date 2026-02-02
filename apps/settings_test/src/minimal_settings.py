"""Minimal settings test - just SettingsPage without Settings class."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Minimal Settings"
    app.width = 300
    app.height = 200

    # Minimal settings page - single tab with just text
    app.settings = nib.SettingsPage(
        title="Preferences",
        width=400,
        height=300,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.Text("Hello Settings"),
            ),
        ],
    )

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Minimal Settings Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
