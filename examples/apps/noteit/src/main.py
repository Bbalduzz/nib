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
        nib.MenuItem("Settings", shortcut="cmd+,", action=lambda: print("Settings")),
        nib.MenuItem("Quit", shortcut="cmd+q", action=app.quit),
    ]

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

    @app.hotkey("ctrl+s")
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
