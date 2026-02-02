"""Settings test - no Settings object, just a simple variable."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug 7"
    app.width = 300
    app.height = 200

    # Just a simple dict, no Settings class
    my_state = {"dark_mode": False}

    def on_toggle_change(value):
        print(f"[DEBUG] Toggle changed to: {value}")
        my_state["dark_mode"] = value
        print(f"[DEBUG] State updated to: {my_state}")

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
                nib.Text("Debug Test 7 - Plain dict"),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
