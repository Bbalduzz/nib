import nib


def main(app: nib.App):
    app.icon = nib.SFSymbol(
        "apple.meditate", rendering_mode=nib.SymbolRenderingMode.HIERARCHICAL
    )
    app.title = "Your Nib app"
    app.menu = [
        nib.MenuItem(
            content=nib.VStack(
                controls=[
                    nib.Text("Custom Item"),
                    nib.Text(
                        "You can place any control you want!",
                        font=nib.Font.CAPTION,
                        foreground_color=nib.Color.WHITE.with_opacity(0.5),
                    ),
                ],
                alignment=nib.Alignment.LEADING,
            ),
            height=35,
        ),
        nib.MenuDivider(),
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
