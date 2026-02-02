"""Settings test with more debug output."""
import nib
import traceback


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug 2"
    app.width = 300
    app.height = 200

    # Create settings
    settings = nib.Settings({
        "dark_mode": False,
    })
    app.register_settings(settings)

    # Status text in main app
    status_text = nib.Text(f"Dark: {settings.dark_mode}")

    def on_toggle_change(value):
        try:
            print(f"[DEBUG] Toggle changed to: {value}")
            settings.dark_mode = value
            print(f"[DEBUG] Settings updated")
            status_text.content = f"Dark: {settings.dark_mode}"
            print(f"[DEBUG] Status text updated - done")
        except Exception as e:
            print(f"[ERROR] Exception in on_toggle_change: {e}")
            traceback.print_exc()

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
                nib.Text("Debug Test 2"),
                status_text,
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
