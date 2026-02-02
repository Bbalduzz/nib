"""Settings test - register but skip initial load."""
import nib


# Monkey-patch to skip initial load
original_load = nib.Settings._load_initial
nib.Settings._load_initial = lambda self: None


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings No Load"
    app.width = 300
    app.height = 200

    # Create and register settings
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
                nib.Text("Settings No Load Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
