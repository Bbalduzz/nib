import nib


def main(app: nib.App):
    app.title = "Divider"
    app.icon = nib.SFSymbol("minus")
    app.width = 300
    app.height = 250

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Section One", font=nib.Font.HEADLINE),
                nib.Text("Content above the divider.", font=nib.Font.BODY),
                nib.Divider(),
                nib.Text("Section Two", font=nib.Font.HEADLINE),
                nib.Text("Content below the divider.", font=nib.Font.BODY),
                nib.Divider(foreground_color=nib.Color.RED),
                nib.Text("Colored divider above.", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY),
            ],
            spacing=8,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
