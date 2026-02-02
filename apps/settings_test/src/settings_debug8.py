"""Settings test - no Settings object, update dict but no second print."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug 8"
    app.width = 300
    app.height = 200

    my_state = {"dark_mode": False}

    def on_toggle_change(value):
        print(f"[DEBUG] Toggle changed to: {value}")
        my_state["dark_mode"] = value
        # NO second print

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
                nib.Text("Debug Test 8"),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
