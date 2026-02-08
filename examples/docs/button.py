import nib


def main(app: nib.App):
    app.title = "Button"
    app.icon = nib.SFSymbol("hand.tap")
    app.width = 300
    app.height = 350

    counter = nib.Text("0", font=nib.Font.TITLE)

    def increment():
        counter.content = str(int(counter.content) + 1)

    def reset():
        counter.content = "0"

    app.build(
        nib.VStack(
            controls=[
                counter,
                nib.Divider(),
                nib.Button("Default", action=increment),
                nib.Button(
                    "Bordered",
                    action=increment,
                    style=nib.ButtonStyle.BORDERED,
                ),
                nib.Button(
                    "Bordered Prominent",
                    action=increment,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                nib.Button(
                    "Destructive",
                    action=reset,
                    role=nib.ButtonRole.DESTRUCTIVE,
                    style=nib.ButtonStyle.BORDERED_PROMINENT,
                ),
                nib.Button("With Icon", icon="plus.circle", action=increment),
                nib.Button("Disabled", action=increment, disabled=True),
            ],
            spacing=10,
            padding=20,
        )
    )


nib.run(main)
