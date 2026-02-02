"""Settings test - callback does NOTHING, not even print."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug 9"
    app.width = 300
    app.height = 200

    def on_toggle_change(value):
        pass  # Literally do nothing

    # Settings page
    app.settings = nib.SettingsPage(
        title="Preferences",
        width=400,
        height=250,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.VStack(
                    controls=[
                        nib.Text("Settings"),
                        nib.Toggle("Dark Mode", is_on=False, on_change=on_toggle_change),
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
                nib.Text("Debug Test 9 - Empty callback"),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
