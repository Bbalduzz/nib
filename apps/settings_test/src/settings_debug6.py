"""Settings test - Settings object created but NOT registered, use directly."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug 6"
    app.width = 300
    app.height = 200

    # Create settings but DON'T register with app
    settings = nib.Settings({
        "dark_mode": False,
    })
    # NOT calling: app.register_settings(settings)

    def on_toggle_change(value):
        print(f"[DEBUG] Toggle changed to: {value}")
        # Just update the cache directly (no persist, no register)
        settings._cache["dark_mode"] = value
        print(f"[DEBUG] Cache updated to: {settings._cache}")

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
                nib.Text("Debug Test 6 - Not registered"),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
