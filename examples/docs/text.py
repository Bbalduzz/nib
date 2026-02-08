import nib


def main(app: nib.App):
    app.title = "Text"
    app.icon = nib.SFSymbol("textformat")
    app.width = 300
    app.height = 350

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Large Title", font=nib.Font.LARGE_TITLE),
                nib.Text("Title", font=nib.Font.TITLE),
                nib.Text("Headline", font=nib.Font.HEADLINE),
                nib.Text("Body text goes here.", font=nib.Font.BODY),
                nib.Text("Caption", font=nib.Font.CAPTION),
                nib.Divider(),
                nib.Text(
                    "Colored text",
                    font=nib.Font.BODY,
                    foreground_color=nib.Color.BLUE,
                ),
                nib.Text(
                    "Bold text",
                    style=nib.TextStyle(font=nib.Font.BODY, bold=True),
                ),
                nib.Text(
                    "This is a long line that will be truncated after two lines of text to demonstrate the line limit feature.",
                    font=nib.Font.BODY,
                    line_limit=2,
                ),
            ],
            spacing=8,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
