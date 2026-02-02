import nib


def main(app: nib.App):
    app.title = "Test"
    app.icon = "star.fill"

    # Simple menu without height first
    app.menu = [
        nib.MenuItem(
            content=nib.Text("Custom Item"),
            height=50,
        ),
        nib.MenuItem("Quit", action=app.quit),
    ]

    app.build(nib.Text("Hello"))


nib.run(main)
