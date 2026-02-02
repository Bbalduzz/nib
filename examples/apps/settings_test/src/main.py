"""Test app for Settings feature."""
import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol("gear")
    app.title = "Settings Test"
    app.width = 300
    app.height = 200

    # Create settings with defaults
    settings = nib.Settings({
        "dark_mode": False,
        "font_size": 14,
        "username": "guest",
    })
    app.register_settings(settings)

    # Current values display
    status_text = nib.Text(f"Dark: {settings.dark_mode}, Font: {settings.font_size}")

    def update_status():
        status_text.content = f"Dark: {settings.dark_mode}, Font: {settings.font_size}"

    # Define settings page with tabs
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
                        nib.Divider(),
                        nib.Toggle(
                            "Dark Mode",
                            is_on=settings.dark_mode,
                            on_change=lambda v: (
                                setattr(settings, "dark_mode", v),
                                update_status(),
                            ),
                        ),
                        nib.HStack(
                            controls=[
                                nib.Text("Font Size:"),
                                nib.Slider(
                                    value=settings.font_size,
                                    min_value=10,
                                    max_value=24,
                                    on_change=lambda v: (
                                        setattr(settings, "font_size", int(v)),
                                        update_status(),
                                    ),
                                ),
                                nib.Text(str(settings.font_size)),
                            ],
                            spacing=8,
                        ),
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
                        nib.Divider(),
                        nib.TextField(
                            "Username",
                            value=settings.username,
                            on_change=lambda v: setattr(settings, "username", v),
                        ),
                    ],
                    spacing=12,
                    padding=20,
                ),
            ),
        ],
    )

    # Main app content
    app.build(
        nib.VStack(
            controls=[
                nib.Text("Settings Test App", font=nib.Font.title),
                nib.Divider(),
                status_text,
                nib.Spacer(),
                nib.Button("Open Settings", action=app.open_settings),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
