"""Simple bundleable example for testing nib build."""

import nib


def main(app):
    app.title = "Bundled App"
    app.icon = nib.SFSymbol("star.fill")

    counter = nib.Text("0")

    def increment():
        counter.content = str(int(counter.content) + 1)

    app.menu = [
        nib.MenuItem("Quit", action=app.quit),
    ]

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Hello from bundled app!", font=nib.Font.title),
                counter,
                nib.Button("Increment", action=increment),
            ],
            spacing=16,
            padding=24,
        )
    )


nib.run(main)
