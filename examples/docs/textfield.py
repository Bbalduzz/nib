import nib


def main(app: nib.App):
    app.title = "TextField"
    app.icon = nib.SFSymbol("character.cursor.ibeam")
    app.width = 300
    app.height = 300

    output = nib.Text("Type something...", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_submit(value):
        output.content = f"Submitted: {value}"

    app.build(
        nib.VStack(
            controls=[
                nib.TextField(
                    placeholder="Default style",
                    on_submit=on_submit,
                ),
                nib.TextField(
                    placeholder="Rounded border",
                    style=nib.TextFieldStyle.ROUNDED_BORDER,
                    on_submit=on_submit,
                ),
                nib.TextField(
                    placeholder="Plain style",
                    style=nib.TextFieldStyle.PLAIN,
                    on_submit=on_submit,
                ),
                nib.SecureField(
                    placeholder="Password",
                    style=nib.TextFieldStyle.ROUNDED_BORDER,
                ),
                nib.Divider(),
                output,
            ],
            spacing=10,
            alignment=nib.Alignment.LEADING,
            padding=20,
        )
    )


nib.run(main)
