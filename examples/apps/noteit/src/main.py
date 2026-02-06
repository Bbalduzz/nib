"""
Noteit - A nib application
"""

import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "text.redaction", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.height = 200
    app.fonts = {
        "Iosevka": "fonts/Iosevka/Iosevka-Regular.ttf",
        "Iosevka-BoldItalic": "fonts/Iosevka/Iosevka-BoldItalic.ttf",
    }
    app.menu = [
        nib.MenuItem(
            content=nib.VStack(
                [
                    nib.Text("No notes saved"),
                    nib.Text(
                        "Here you'll see the history",
                        font=nib.Font.CAPTION,
                        foreground_color=nib.Color.WHITE.with_opacity(0.5),
                    ),
                ],
                alignment=nib.Alignment.LEADING,
                margin={"leading": -40},
            ),
            height=35,
        ),
        nib.MenuDivider(),
        nib.MenuItem(
            "Settings",
            shortcut="cmd+,",
            action=lambda: app.settings.open(),
        ),
        nib.MenuItem("Quit", shortcut="cmd+q", action=app.quit),
    ]

    settings = nib.Settings(
        {
            "width": 280,
            "height": 200,
            "font": "Iosevka",
            "font_size": 14,
            "accent_color": "#ED9516",
        }
    )
    app.register_settings(settings)

    def update_status():
        app.width = settings.width
        app.height = settings.height
        app.update()

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
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Popup width"),
                                        nib.Slider(
                                            label="width",
                                            value=280,
                                            min_value=0,
                                            max_value=600,
                                            on_change=lambda v: (
                                                setattr(settings, "width", v),
                                                update_status(),
                                            ),
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
                                            on_change=lambda v: (
                                                setattr(settings, "height", v),
                                                update_status(),
                                            ),
                                        ),
                                    ]
                                ),
                                nib.TextField(
                                    "Accent Color",
                                    value=settings.accent_color,
                                    on_submit=lambda v: (
                                        setattr(settings, "accent_color", v),
                                        update_status(),
                                    ),
                                ),
                            ],
                            header="Appearance",
                        )
                    ],
                    style=nib.FormStyle.GROUPED,
                ),
            ),
            nib.SettingsTab(
                "Text",
                icon="textformat.size",
                content=nib.Form(
                    style=nib.FormStyle.GROUPED,
                    controls=[
                        nib.Section(
                            header="Text Appearance",
                            controls=[
                                nib.HStack(
                                    [
                                        nib.Text("Font size"),
                                        nib.Slider(
                                            label="size",
                                            value=14,
                                            min_value=5,
                                            max_value=24,
                                            on_change=lambda v: (
                                                setattr(settings, "width", v),
                                                update_status(),
                                            ),
                                        ),
                                    ]
                                ),
                                nib.Picker(
                                    label="Font",
                                    options=["Arial", "Helvetica", "Times New Roman"],
                                    on_change=lambda v: (
                                        setattr(settings, "font", v),
                                        update_status(),
                                    ),
                                ),
                            ],
                        )
                    ],
                ),
            ),
        ],
    )

    word_count = nib.Text(
        "0",
        font=nib.Font.custom("Iosevka", size=11),
        foreground_color=nib.Color("#4D535E"),
    )

    text_editor = nib.TextEditor(
        style=nib.TextEditorStyle(
            font=nib.Font.custom("Iosevka", size=13, weight=nib.FontWeight.BOLD),
            foreground_color=nib.Color.WHITE.with_opacity(0.7),
        ),
        content_background=nib.Color.BLACK.with_opacity(0),
        on_change=lambda text: setattr(word_count, "content", str(len(text.split()))),
    )

    @app.hotkey("ctrl+p")
    def save_note():
        with open("notes.txt", "w") as file:
            file.write(text_editor.text)

    @app.hotkey("ctrl+l")
    def create_link():
        # use lzma compression and url encoding
        print(text_editor.text[:10])
        ...

    commands_row = nib.HStack(
        controls=[
            nib.HStack(
                controls=[
                    nib.Text(
                        "^s",
                        font=nib.Font.custom(
                            "Iosevka-BoldItalic", weight=nib.FontWeight.BOLD, size=13
                        ),
                        foreground_color=nib.Color("#ED9516"),
                    ),
                    nib.Text(
                        "ave",
                        font=nib.Font.custom("Iosevka", size=13),
                    ),
                ],
                spacing=0.5,
                on_click=save_note,
            ),
            nib.HStack(
                controls=[
                    nib.Text(
                        "^l",
                        font=nib.Font.custom(
                            "Iosevka-BoldItalic", weight=nib.FontWeight.BOLD, size=13
                        ),
                        foreground_color=nib.Color("#ED9516"),
                    ),
                    nib.Text(
                        "ink",
                        font=nib.Font.custom("Iosevka", size=13),
                    ),
                ],
                spacing=0.5,
                on_click=create_link,
            ),
        ],
        spacing=12,
    )

    app.build(
        nib.VStack(
            controls=[
                text_editor,
                nib.HStack([word_count, nib.Spacer(), commands_row]),
            ],
            padding={"leading": 14, "trailing": 14, "top": 14, "bottom": 10},
        )
    )


nib.run(main, assets_dir="assets")
