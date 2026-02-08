import nib


def main(app: nib.App):
    app.title = "SecureField"
    app.icon = nib.SFSymbol("lock")
    app.width = 300
    app.height = 250

    status = nib.Text("", font=nib.Font.CAPTION, foreground_color=nib.Color.SECONDARY)

    def on_submit(value):
        status.content = f"Password length: {len(value)}"

    app.build(
        nib.VStack(
            controls=[
                nib.Text("Login", font=nib.Font.TITLE),
                nib.TextField(
                    placeholder="Username",
                    style=nib.TextFieldStyle.ROUNDED_BORDER,
                ),
                nib.SecureField(
                    placeholder="Password",
                    style=nib.TextFieldStyle.ROUNDED_BORDER,
                    on_submit=on_submit,
                ),
                nib.Button(
                    "Sign In",
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                status,
            ],
            spacing=10,
            padding=20,
        )
    )


nib.run(main)
