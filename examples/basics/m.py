import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "apple.meditate", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.title = "Your Nib app"
    app.menu = [
        nib.MenuItem("Quit", shortcut="cmd+q", action=app.quit),
    ]

    count = nib.Text("0", font=nib.Font.TITLE2)

    def increment():
        count.content = str(int(count.content) + 1)

    def decrement():
        count.content = str(int(count.content) - 1)

    app.build(
        nib.HStack(
            controls=[
                nib.Button(content=nib.SFSymbol("minus"), action=decrement),
                count,
                nib.Button(content=nib.SFSymbol("plus"), action=increment),
            ]
        )
    )


nib.run(main)
