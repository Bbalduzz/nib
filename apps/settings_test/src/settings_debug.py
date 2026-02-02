"""Settings test with debug output."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Debug"
    app.width = 300
    app.height = 200

    # Create settings
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
    })
    app.register_settings(settings)

    # Status text in main app
    status_text = nib.Text(f"Dark: {settings.dark_mode}")

    def on_toggle_change(value):
        print(f"[DEBUG] Toggle changed to: {value}")
        settings.dark_mode = value
        status_text.content = f"Dark: {settings.dark_mode}"
        print(f"[DEBUG] Status updated to: {status_text.content}")

    # Settings page with debug callbacks
    app.settings = nib.SettingsPage(
        title="Preferences",
        width=450,
        height=300,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.VStack(
                    controls=[
                        nib.Text("General Settings", font=nib.Font.headline),
                        nib.Toggle(
                            "Dark Mode",
                            is_on=settings.dark_mode,
                            on_change=on_toggle_change,
                        ),
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
                nib.Text("Settings Debug Test", font=nib.Font.title),
                status_text,
                nib.Spacer(),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
