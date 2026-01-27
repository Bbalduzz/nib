import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

import nib as nib


def main(app: nib.App):
    app.title = "My App"
    app.icon = nib.SFSymbol("star")

    # Right-click menu
    app.menu = [
        nib.MenuItem(
            "Copy", action=lambda: app.set_clipboard("copied!"), icon="doc.on.doc"
        ),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

    # Global hotkey
    @app.hotkey("cmd+shift+n")
    def show_notification():
        print("shortcut pressed!")
        app.notify("Hello!", "Hotkey pressed")

    # Drop zone
    def handle_drop(files):
        print(f"Dropped: {files}")

    app.build(
        nib.VStack(
            controls=[nib.Text("Drop files here")],
            on_drop=handle_drop,
            padding=20,
        )
    )


nib.run(main)
"""
def main(app: nib.App):
    app.title = "nib"
    app.icon = nib.SFSymbol("pencil.and.outline")  # or a nib.Image(src="...")
    app.show_quit_item = True
    app.width = 300
    app.height = 500

    app.menu = [
        nib.MenuItem("Settings", icon="gear"),
        nib.MenuItem("Check for Updates"),
        nib.MenuDivider(),
        nib.MenuItem("Quit", action=app.quit),
    ]

    input = nib.Text("0")

    def minus_click():
        input.content = str(int(input.content) - 1)

    def plus_click():
        input.content = str(int(input.content) + 1)

    app.build(
        nib.VStack(
            [
                nib.Text("Demo", font=nib.Font.system(14, nib.FontWeight.bold)),
                nib.HStack(
                    controls=[
                        nib.Button(
                            content=nib.SFSymbol(
                                "minus",
                                weight="bold",
                            ),
                            action=minus_click,
                        ),
                        input,
                        nib.Button(
                            content=nib.SFSymbol(
                                "plus",
                                weight="bold",
                            ),
                            action=plus_click,
                        ),
                    ],
                ),
            ]
        )
    )


nib.run(main)
"""
