"""Settings test with interactive controls."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Controls"
    app.width = 300
    app.height = 200

    # Settings page with controls
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
                        nib.Toggle(
                            "Dark Mode",
                            is_on=False,
                            on_change=lambda v: print(f"Dark mode: {v}"),
                        ),
                        nib.Slider(
                            value=14,
                            min_value=10,
                            max_value=24,
                            on_change=lambda v: print(f"Font size: {v}"),
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
                nib.Text("Settings Controls Test", font=nib.Font.title),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
