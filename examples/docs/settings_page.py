import nib


def main(app: nib.App):
    app.title = "Settings"
    app.icon = nib.SFSymbol("gear")
    app.width = 300
    app.height = 200

    settings = nib.Settings({"dark_mode": False, "volume": 50, "username": "guest"})
    app.register_settings(settings)


import nib

FONT_OPTIONS = [
    "Iosevka",
    "System",
    "Menlo",
    "Monaco",
    "SF Mono",
    "Courier New",
    "Helvetica Neue",
]

WEIGHT_OPTIONS = ["thin", "light", "regular", "medium", "semibold", "bold", "heavy"]

WEIGHT_MAP = {
    "thin": nib.FontWeight.THIN,
    "light": nib.FontWeight.LIGHT,
    "regular": nib.FontWeight.REGULAR,
    "medium": nib.FontWeight.MEDIUM,
    "semibold": nib.FontWeight.SEMIBOLD,
    "bold": nib.FontWeight.BOLD,
    "heavy": nib.FontWeight.HEAVY,
}


def main(app: nib.App):
    app.title = "Settings"
    app.icon = nib.SFSymbol("gear")
    app.width = 300
    app.height = 200

    settings = nib.Settings({"dark_mode": False, "volume": 50, "username": "guest"})
    app.register_settings(settings)

    app.settings = nib.SettingsPage(
        title="Preferences",
        width=450,
        height=350,
        tabs=[
            nib.SettingsTab(
                "General",
                icon="gear",
                content=nib.Form(
                    controls=[
                        nib.Section(
                            header="Info",
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Database"),
                                        nib.Spacer(),
                                        nib.Text(
                                            "path/to/database.db",
                                            style=nib.TextStyle(
                                                color=nib.Color.WHITE.with_opacity(0.5)
                                            ),
                                        ),
                                    ],
                                    on_click=lambda _: print(
                                        "open filepicker and select new database path"
                                    ),
                                ),
                            ],
                        ),
                        nib.Section(
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Popup width"),
                                        nib.Slider(
                                            label="width",
                                            value=280,
                                            min_value=0,
                                            max_value=600,
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Popup height"),
                                        nib.Slider(
                                            label="height",
                                            value=300,
                                            min_value=0,
                                            max_value=600,
                                        ),
                                    ]
                                ),
                                nib.TextField(
                                    "Accent Color",
                                    value="#ffffff",
                                ),
                            ],
                            header="Appearance",
                        ),
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
            nib.SettingsTab(
                "Editor",
                icon="textformat.size",
                content=nib.Form(
                    style=nib.FormStyle.GROUPED,
                    controls=[
                        nib.Section(
                            header="Typography",
                            controls=[
                                nib.Picker(
                                    label="Font",
                                    selection="Iosevka",
                                    options=FONT_OPTIONS,
                                ),
                                nib.Picker(
                                    label="Weight",
                                    selection="regular",
                                    options=WEIGHT_OPTIONS,
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Font size"),
                                        nib.Slider(
                                            label="size",
                                            value=14,
                                            min_value=8,
                                            max_value=24,
                                            step=1,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        nib.Section(
                            header="Appearance",
                            controls=[
                                nib.TextField(
                                    "Text color",
                                    value="#ffffff",
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Text opacity"),
                                        nib.Slider(
                                            label="opacity",
                                            value=0.8,
                                            min_value=0.0,
                                            max_value=1.0,
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Editor bg opacity"),
                                        nib.Slider(
                                            label="bg opacity",
                                            value=0.0,
                                            min_value=0.0,
                                            max_value=1.0,
                                        ),
                                    ]
                                ),
                                nib.HStack(
                                    [
                                        nib.Text("Line spacing"),
                                        nib.Slider(
                                            label="spacing",
                                            value=1,
                                            min_value=0,
                                            max_value=12,
                                            step=1,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Open Settings to see the preferences window."),
                nib.Button(
                    "Open Settings",
                    action=lambda: app.settings.open(),
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
            ],
            spacing=12,
            padding=20,
        )
    )


nib.run(main)
